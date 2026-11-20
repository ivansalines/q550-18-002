"""Generate held-out endpoint-preserved chronological/scrambled Q550 observables.

This ORACLE alone imports the verified original Q550 ODE and the archive. The
estimator robust_math_v18_24 sees ONLY reduced sampled data arrays. Anchor
shifts also change baseline posture: they are not pure phase interventions.
"""
from pathlib import Path
import sys,json,zipfile,argparse
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from checkpoint_io_v18_24 import read
from checkpoint_io_v18_21 import PREFIX as PREFIX20
from frozen_preflight import observers
from blind_experiment import initial_directions,OBSERVERS
from blind_math import HISTORY,HORIZONS
from robust_math_v18_24 import evaluate,ANCHORS
import q550_state_impulse_response_v13 as original

def integrate(f,t0,t1,state,grid):
    sol=solve_ivp(f,(float(t0),float(t1)),state,t_eval=np.asarray(grid,float),method='DOP853',rtol=5e-11,atol=6e-12,max_step=.04)
    if not sol.success:raise RuntimeError(sol.message)
    return sol.y.T

def generate(f,anchor,center,v,amplitude):
    past=np.asarray(anchor+HISTORY,float)
    future=np.asarray(anchor+HORIZONS,float)
    ini=center.copy();ini[:10]+=amplitude*np.asarray(v,float)
    back=integrate(f,anchor,float(past[0]),ini,past[::-1])
    forward=integrate(f,anchor,float(future[-1]),ini,np.r_[anchor,future])
    combined=np.vstack((back[::-1],forward[1:]))
    assert combined.shape==(len(HISTORY)+len(HORIZONS),11)
    return combined

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base-root',type=Path,default=original.DEFAULT_BASE)
    args=parser.parse_args()
    verified_sources={}
    for name,(filename,digest) in original.DEPENDENCIES.items():
        target=args.base_root/filename
        if not target.exists():raise FileNotFoundError('Pinned original Q550 source absent '+str(target))
        if original.hash_file(target)!=digest:raise RuntimeError('ODE source SHA256 mismatch '+str(target))
        verified_sources[name]={'path':str(target),'sha256':digest}
    D,prov,parent=read();d=D['tight'];Hs=observers(d)
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        seeds=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    direction_data=initial_directions({s['name']:s['seed'] for s in seeds})
    original_audit=original.load_module(args.base_root/original.DEPENDENCIES['audit'][0],'v1824_audit')
    support=original.load_module(args.base_root/original.DEPENDENCIES['support'][0],'v1824_support')
    params=original_audit.ModelParameters(gamma_rho=.3)
    kappa0=(55./6.)*(10./550.)
    slope=float(d['slope']);y0=np.asarray(d['source_state_11D'],float)
    def rhs(t,y):return slope*np.asarray(support.support_rhs_float(np.asarray(y,float),kappa0=kappa0,params=params,audit=original_audit),float)
    anchor_states=integrate(rhs,0.,4.5,y0,np.array(ANCHORS))
    baseline={a:generate(rhs,a,center,np.zeros(10),0.) for a,center in zip(ANCHORS,anchor_states)}
    # Provenance of the reference phase and posture at each anchor.
    ref_phase={str(a):float(center[-1]) for a,center in zip(ANCHORS,anchor_states)}
    P=CubicSpline(np.asarray(d['xi_nodes']),np.asarray(d['P_full11D'][:,:10,:10]),axis=0)
    data={o:{} for o in OBSERVERS}
    common=direction_data['material3']
    common_random={split:common[split][:-1] if split=='test' else common[split]
                   for split in ('train','val','test')}
    n_integrations=len(ANCHORS) # Count baseline independently integrated states.
    for anchor,center in zip(ANCHORS,anchor_states):
        raw={}
        for split,U in common_random.items():
            if anchor!=4.0 and split!='test':continue
            eps=1e-5 if split in ('train','val') else 3e-6
            chunks=[]
            for i,direction in enumerate(U):
                y=generate(rhs,anchor,center,direction,eps)
                err=float(np.max(np.abs(y[:,10]-baseline[anchor][:,10])))
                if err>1e-8:raise RuntimeError('Unwanted phase mismatch '+str(err))
                chunks.append((y[:,:10]-baseline[anchor][:,:10])/eps)
                n_integrations+=1
            raw[split]=np.asarray(chunks)
            print('ORIGINAL Q550',anchor,split,len(U),flush=True)
        for obs in OBSERVERS:
            H=Hs[obs];subset={}
            for split,arr in raw.items():
                measured=np.einsum('ab,ntb->nta',H,arr)
                subset[split]=(measured[:,:len(HISTORY)],measured[:,len(HISTORY):].reshape(len(measured),-1))
            matched=direction_data[obs]['matched_seed'].copy()
            if anchor!=4.0:
                # Trajectory-comoving transport of the original hidden seed;
                # does not claim local endpoint or jet matching at shifted anchor.
                shifted=P(anchor)@np.linalg.solve(P(4.),matched)
                matched=shifted/np.linalg.norm(shifted)
            y=generate(rhs,anchor,center,matched,3e-6)
            n_integrations+=1
            if float(np.max(abs(y[:,10]-baseline[anchor][:,10])))>1e-8:raise RuntimeError('Matched phase mismatch')
            observed=((y[:,:10]-baseline[anchor][:,:10])/3e-6)@H.T
            x=observed[:len(HISTORY)][None]
            future=observed[len(HISTORY):].reshape(1,-1)
            subset['test']=(np.concatenate((subset['test'][0],x),axis=0),
                             np.concatenate((subset['test'][1],future),axis=0))
            data[obs][anchor]=subset
    summary=evaluate(data,'original',{
        'status':'ORIGINAL_Q550_ENDPOINT_PRESERVED_BLIND_NONLINEAR_VALIDATION_COMPLETED',
        'original_ode_pinned_sources':verified_sources,
        'parent_server_sha256':prov['v18_23_server_sha256'],
        'train_amp':1e-5,'validation_amp':1e-5,'heldout_amp':3e-6,
        'n_original_q550_integrations':n_integrations,
        'one_shared_test_set_at_all_three_anchors':True,
        'reference_phase_coordinates':ref_phase,
        'shifted_observations':'phase and material posture both shift',
        'same_observer_projection_at_all_anchors':True})
    (ROOT/'results/original_ode_robustness_proof.json').write_text(json.dumps({
       'version':'v18.24','status':'ORIGINAL_Q550_ENDPOINT_PRESERVED_BLIND_NONLINEAR_VALIDATION_COMPLETED',
       'verified_sources':verified_sources,'parent_v18_23_status':parent['status'],
       'model_blind_at_fit_and_inference':True,
       'synthetic_sensor_noise':True,
       'independent_nonlinear_ode_integrations':n_integrations,
       'phase_coordinates':ref_phase,'off_constraint_diagnostic':True,
       'important_limitation':'Phase/posture shift is not an intervention of pure clock phase.'},indent=2)+'\n')
if __name__=='__main__':main()
