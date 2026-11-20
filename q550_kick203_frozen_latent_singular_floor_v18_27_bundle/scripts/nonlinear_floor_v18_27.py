"""Targeted DOP853 accuracy scan for the original Q550 nonlinear +/- probes.

Original pinned RHS files are checked for exact SHA256. This script does NOT
repeat the 400-orbit preparation or the 1,596 integrations of v18.26. It
reintegrates a small set of +/- seeds under two integration tolerances.
Inter-tier disagreement is an empirical numerical FLOOR INDICATOR, not a
rigorous error bound. Never certify a material quadratic law from it alone.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,zipfile
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from singular_subspace_v18_27 import authentic_data
from amplitude_math_v18_26 import AMPLITUDES,OBSERVERS
from transport_math_v18_25 import ANCHORS
from blind_math import HISTORY,HORIZONS
import q550_state_impulse_response_v13 as original

TIERS=(('reference',5e-11,6e-12,.04),('tight',3e-13,3e-14,.01))


def oracle_setup(base_root):
    for key,(filename,digest) in original.DEPENDENCIES.items():
        file=base_root/filename
        if not file.exists() or original.hash_file(file)!=digest:
            raise RuntimeError('Pinned Q550 source absent or changed: '+str(file))
    # Authenticate previous nonlinear run, and unpack its authenticated parent
    # only to recover the original checkpoint needed to restart short orbits.
    _,parent,_,_,_=authentic_data()
    with zipfile.ZipFile(ROOT/'inputs/v18_26_original_server_sendback.zip') as z:
        name='q550_kick203_vanishing_amplitude_latent_transport_v18_26_bundle/inputs/v18_25_original_server_sendback.zip'
        cache=ROOT/'.runtime';cache.mkdir(exist_ok=True)
        (cache/'v18_25_original_server_sendback.zip').write_bytes(z.read(name))
    import checkpoint_io_v18_26 as checkpoint
    checkpoint.SOURCE=ROOT/'.runtime/v18_25_original_server_sendback.zip'
    d=checkpoint.read()[0]['tight']
    import frozen_preflight
    Hs=frozen_preflight.observers(d)
    from checkpoint_io_v18_21 import PREFIX as PREFIX20
    from blind_experiment import initial_directions
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        seeds=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    directions=initial_directions({r['name']:r['seed'] for r in seeds})
    audit=original.load_module(base_root/original.DEPENDENCIES['audit'][0],'v1827_audit')
    support=original.load_module(base_root/original.DEPENDENCIES['support'][0],'v1827_support')
    params=audit.ModelParameters(gamma_rho=.3)
    kappa0=(55./6.)*(10./550.);slope=float(d['slope'])
    def rhs(t,y):
        return slope*np.asarray(support.support_rhs_float(np.asarray(y,float),kappa0=kappa0,
                          params=params,audit=audit),float)
    return d,Hs,directions,rhs,parent


def ode(rhs,a,b,state,grid,method):
    name,rtol,atol,max_step=method
    sol=solve_ivp(rhs,(float(a),float(b)),np.asarray(state,float),
                  t_eval=np.asarray(grid,float),method='DOP853',rtol=rtol,
                  atol=atol,max_step=max_step)
    if not sol.success:raise RuntimeError(name+': '+sol.message)
    return sol.y.T


def pair_run(rhs,anchor,center,seed,eps,tier):
    def sample(direction):
        init=center.copy();init[:10]+=eps*direction
        past=anchor+HISTORY; future=anchor+HORIZONS
        back=ode(rhs,anchor,past[0],init,past[::-1],tier)
        forward=ode(rhs,anchor,future[-1],init,np.r_[anchor,future],tier)
        return np.vstack((back[::-1],forward[1:]))
    base=sample(np.zeros(10))
    plus=sample(seed);minus=sample(-seed)
    if max(np.max(abs(plus[:,10]-base[:,10])),np.max(abs(minus[:,10]-base[:,10])))>1e-8:
        raise RuntimeError('Clock mismatch')
    return plus,minus,base


def summarize_pair(pair,H,eps):
    plus,minus,base=pair
    # First differences on all 10 source coordinates; avoid false inference
    # from subtraction at the 4,000-unit state scale at tiny eps.
    p=((plus[:,:10]-base[:,:10])/eps)@H.T
    m=((minus[:,:10]-base[:,:10])/eps)@H.T
    return (p-m)/2.,(p+m)/2.


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--base-root',type=Path,default=original.DEFAULT_BASE)
    ap.add_argument('--only-observer',choices=list(OBSERVERS)+['all'],default='all')
    args=ap.parse_args()
    d,Hs,directions,rhs,parent=oracle_setup(args.base_root)
    names=OBSERVERS if args.only_observer=='all' else (args.only_observer,)
    centers={};counts=0;row=[];summaries={}
    for tier in TIERS:
        center=ode(rhs,0.,4.5,np.asarray(d['source_state_11D'],float),np.array(ANCHORS),tier)
        centers[tier[0]]=dict(zip(ANCHORS,center)); counts+=1
    for obs in names:
      for a in ANCHORS:
        seed=directions[obs]['matched_seed'].copy()
        if a!=4.:
            from scipy.interpolate import CubicSpline
            P=CubicSpline(np.asarray(d['xi_nodes']),np.asarray(d['P_full11D'][:,:10,:10]),axis=0)
            seed=P(a)@np.linalg.solve(P(4.),seed);seed/=np.linalg.norm(seed)
        H=Hs[obs]
        for eps in AMPLITUDES:
            result={}
            for tier in TIERS:
                pair=pair_run(rhs,a,centers[tier[0]][a],seed,eps,tier)
                odd,even=summarize_pair(pair,H,eps)
                result[tier[0]]=(odd,even)
                counts+=3
            odd0,even0=result['reference'];odd1,even1=result['tight']
            r=lambda x:float(np.sqrt(np.mean(x*x)))
            even_disagreement=r(even0-even1)
            odd_disagreement=r(odd0-odd1)
            record={'observer':obs,'anchor':a,'amplitude':eps,
                'reference_even_rms':r(even0),'tight_even_rms':r(even1),
                'even_inter_tier_rms_disagreement':even_disagreement,
                'even_signal_over_tier_difference':r(even1)/max(even_disagreement,1e-30),
                'reference_odd_rms':r(odd0),'tight_odd_rms':r(odd1),
                'odd_inter_tier_rms_disagreement':odd_disagreement,
                'tight_even_raw_eps_rms':eps*r(even1),
                'inter_tier_is_not_rigorous_bound':True}
            row.append(record)
            print('FLOOR',obs,'anchor',a,'eps',eps,
                  'even_tight',f'{r(even1):.3e}','intertier',f'{even_disagreement:.3e}',flush=True)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    with (out/'original_tight_floor_comparison_v18_27.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(row[0]));w.writeheader();w.writerows(row)
    proof={'version':'v18.27','status':'ORIGINAL_Q550_HIGH_PRECISION_NUMERICAL_FLOOR_SCAN_COMPLETED',
       'parent_server_sha256':parent['parent_sha256'],'authenticated_original_rhs':True,
       'tiers':[{'name':n,'rtol':r,'atol':a,'max_step':s} for n,r,a,s in TIERS],
       'new_original_ode_integrations':counts,'rows':len(row),'observers':list(names),
       'amplitudes':list(AMPLITUDES),'anchors':list(ANCHORS),
       'baseline_reintegrated_for_each_tier':True,
       'inter_tier_disagreement_not_a_mathematical_error_bound':True,
       'same_phase_in_pair':True,
       'not_a_certification_of_constitutive_hysteresis':True}
    (out/'original_high_precision_floor_proof_v18_27.json').write_text(json.dumps(proof,indent=2)+'\n')
    print('ORIGINAL_V18_27_FLOOR_COMPLETED',len(row),'rows',counts,'short ODE integrations')

if __name__=='__main__':main()
