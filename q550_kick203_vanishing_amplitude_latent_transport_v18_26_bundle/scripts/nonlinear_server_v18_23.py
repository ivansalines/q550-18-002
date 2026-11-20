"""Original-Q550 independent nonlinear trajectory producer for model-blind predictor.

The fitting procedure in blind_math.py never reads this module, its ODE, state,
Jacobian, tangent propagator or the perturbation directions.
"""
from pathlib import Path
import sys,json,zipfile,argparse,hashlib
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from checkpoint_io_v18_23 import read
from checkpoint_io_v18_21 import PREFIX as PREFIX20
from frozen_preflight import observers
from blind_math import HISTORY,HORIZONS
from blind_experiment import initial_directions,run_experiment,OBSERVERS
import q550_state_impulse_response_v13 as original

def integrate(f,t0,t1,state,grid):
    sol=solve_ivp(f,(t0,t1),state,t_eval=np.asarray(grid),method='DOP853',rtol=5e-11,atol=6e-12,max_step=.04)
    if not sol.success:raise RuntimeError(sol.message)
    return sol.y.T

def generate(f,state4,delta,amplitude,past,future):
    ini=state4.copy();ini[:10]+=amplitude*delta
    back=integrate(f,4.,float(past[0]),ini,past[::-1])
    forward=integrate(f,4.,float(future[-1]),ini,np.r_[4.,future])
    return np.vstack([back[::-1],forward[1:]])

def main():
    p=argparse.ArgumentParser();p.add_argument('--base-root',type=Path,default=original.DEFAULT_BASE)
    args=p.parse_args()
    deps={}
    for name,(filename,digest) in original.DEPENDENCIES.items():
        target=args.base_root/filename
        if not target.exists():raise FileNotFoundError('Original pinned file absent '+str(target))
        if original.hash_file(target)!=digest:raise RuntimeError('ODE source checksum mismatch '+str(target))
        deps[name]=dict(path=str(target),sha256=digest)
    D,prov,prior_proof=read();d=D['tight'];Hs=observers(d)
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        records=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    hidden={p['name']:p['seed'] for p in records}
    directions=initial_directions(hidden)
    audit=original.load_module(args.base_root/original.DEPENDENCIES['audit'][0],'v1823_audit')
    support=original.load_module(args.base_root/original.DEPENDENCIES['support'][0],'v1823_support')
    params=audit.ModelParameters(gamma_rho=.3);kappa0=(55./6.)*(10./550.)
    slope=float(d['slope']);y0=np.asarray(d['source_state_11D'],float)
    def f(x,y):return slope*np.asarray(support.support_rhs_float(np.asarray(y,float),kappa0=kappa0,params=params,audit=audit),float)
    center=integrate(f,0.,4.,y0,[4.])[-1]
    # Canonical temporal grid; all sample times distinct; same for train and test.
    past=4.+HISTORY
    future=4.+HORIZONS
    alltimes=np.r_[past,future]
    baseline=generate(f,center,np.zeros(10),0.,past,future)
    # Every observer gets THE SAME disjoint trajectories, with a matched hidden
    # probe appended to its own test group (three extra integrations total).
    base_dirs=directions['material3']
    n_train=len(base_dirs['train']);n_val=len(base_dirs['val']);n_test_random=len(base_dirs['test'])-1
    common=np.vstack([base_dirs['train'],base_dirs['val'],base_dirs['test'][:-1]])
    raw={}
    for split,ind in [('train',slice(0,n_train)),('val',slice(n_train,n_train+n_val)),
                      ('test',slice(n_train+n_val,n_train+n_val+n_test_random))]:
        eps=1e-5 if split in ('train','val') else 3e-6
        samples=[]
        for v in common[ind]:
            pert=generate(f,center,v,eps,past,future)
            if np.max(abs(pert[:,10]-baseline[:,10]))>1e-8:raise RuntimeError('Phase difference')
            samples.append((pert[:,:10]-baseline[:,:10])/eps)
        raw[split]=np.asarray(samples)
    datasets={}
    for key in OBSERVERS:
        data={};H=Hs[key]
        for split in ('train','val','test'):
            obs=np.einsum('ab,ntb->nta',H,raw[split])
            data[split]=(obs[:,:len(past)],obs[:,len(past):].reshape(len(obs),-1))
        probe=directions[key]['matched_seed']
        match=generate(f,center,probe,3e-6,past,future)
        reduced=(match[:,:10]-baseline[:,:10])/3e-6@H.T
        data['test']=(np.concatenate([data['test'][0],reduced[:len(past)][None]],axis=0),
            np.concatenate([data['test'][1],reduced[len(past):].reshape(1,-1)],axis=0))
        datasets[key]=data
    summary=run_experiment(datasets,'ORIGINAL_Q550_MODEL_BLIND_NONLINEAR_TEST_COMPLETED',
      {'original_q550_pinned_sources':deps,'parent_sha256':prov['v18_22_server_sha256'],
       'parent_original_nonlinear_status':prior_proof['status'],
       'sampling_window':'xi 3.5 ... 5.0, match xi 4',
       'train_eps':1e-5,'validation_eps':1e-5,'heldout_eps':3e-6,
       'train_val_test_independent_directions':True,
       'nonlinear_trajectories':len(common)+len(OBSERVERS)+1,
       'probes':'Random 10D perturbations + matched hidden seeds; all generated from original ODE'},True)
    (ROOT/'results/original_ode_blind_summary.json').write_text(json.dumps({
      'version':'v18.23','status':'ORIGINAL_Q550_MODEL_BLIND_NONLINEAR_TEST_COMPLETED',
      'original_sources':deps,'parent_status':prior_proof['status'],
      'sensor_only_estimator':True,'train_test_disjoint':True,
      'different_amplitude_heldout':True,'number_of_original_nonlin_trajectories':len(common)+len(OBSERVERS)+1,
      'warning':'Predictive success for diagnostic reduced observables does not demonstrate physical constitutive hysteresis or metric invariance.'},indent=2)+'\n')
if __name__=='__main__':main()
