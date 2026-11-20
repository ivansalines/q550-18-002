"""Certified-lineage frozen tangent preflight; NOT independent nonlinear proof."""
from pathlib import Path
import json,zipfile,sys
import numpy as np
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from checkpoint_io_v18_24 import read
from checkpoint_io_v18_21 import PREFIX as PREFIX20
from frozen_preflight import observers
from blind_experiment import initial_directions,OBSERVERS
from blind_math import HISTORY,HORIZONS
from robust_math_v18_24 import evaluate,ANCHORS

def make():
    D,prov,parentproof=read();d=D['tight'];Hs=observers(d)
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        records=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    hidden={r['name']:r['seed'] for r in records}
    directions=initial_directions(hidden)
    xi=np.asarray(d['xi_nodes'],float)
    P=np.asarray(d['P_full11D'][:,:10,:10],float)
    interp=CubicSpline(xi,P,axis=0)
    assert min(xi)<=3.0 and max(xi)>=5.5
    results={obs:{} for obs in OBSERVERS}
    for anchor in ANCHORS:
        p_anchor=interp(anchor)
        B=interp(np.r_[anchor+HISTORY,anchor+HORIZONS])@np.linalg.inv(p_anchor)
        if B.shape!=(len(HISTORY)+len(HORIZONS),10,10):raise RuntimeError('Bad propagator stencil')
        for obs in OBSERVERS:
            H=Hs[obs];U=directions[obs]
            data={}
            for split in ('train','val','test'):
                if split!='test' and anchor!=4.:continue
                if split=='test':
                    samples=U['test'].copy()
                    if anchor!=4.:
                        # Transport and normalize the archived hidden direction to a
                        # shifted reference; still NOT a locally jet-matched seed.
                        seed=samples[-1]
                        shifted=interp(anchor)@np.linalg.solve(interp(4.0),seed)
                        samples[-1]=shifted/np.linalg.norm(shifted)
                else:samples=U[split]
                measured=np.einsum('ab,tbc,nc->nta',H,B,samples)
                data[split]=(measured[:,:len(HISTORY)],measured[:,len(HISTORY):].reshape(len(samples),-1))
            results[obs][anchor]=data
    return results,prov,parentproof

if __name__=='__main__':
    ds,prov,proof=make()
    evaluate(ds,'frozen',{'data_type':'ORIGINAL_Q550_FROZEN_TANGENT_ONLY',
       'parent_sha256':prov['v18_23_server_sha256'],'parent_status':proof['status'],
       'source_grid':'CubicSpline on authenticated propagator checkpoints',
       'phase_shift_is_also_posture_shift':True})
