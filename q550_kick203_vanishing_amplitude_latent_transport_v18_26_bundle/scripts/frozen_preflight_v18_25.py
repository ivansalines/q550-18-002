"""v18.25 frozen tangent preflight; not independent original nonlinear evidence."""
from pathlib import Path
import json,zipfile,sys
import numpy as np
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'reference')]
from checkpoint_io_v18_25 import read
from checkpoint_io_v18_21 import PREFIX as PREFIX20
from frozen_preflight import observers
from blind_experiment import initial_directions,OBSERVERS
from blind_math import HISTORY,HORIZONS
from transport_math_v18_25 import evaluate,ANCHORS,CAL_N

def make():
    D,prov,previous=read();d=D['tight'];Hs=observers(d)
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        records=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    directions=initial_directions({r['name']:r['seed'] for r in records})
    xi=np.asarray(d['xi_nodes'],float)
    interp=CubicSpline(xi,np.asarray(d['P_full11D'][:,:10,:10],float),axis=0)
    if min(xi)>3. or max(xi)<5.5:raise RuntimeError('Insufficient certified xi support')
    out={obs:{} for obs in OBSERVERS}
    for anchor in ANCHORS:
        propagator=interp(np.r_[anchor+HISTORY,anchor+HORIZONS])@np.linalg.inv(interp(anchor))
        for obs in OBSERVERS:
            H=Hs[obs];sets={}
            for split in (('train','val','test') if anchor==4. else ('cal','test')):
                if split=='cal':
                    vectors=directions[obs]['train'][:CAL_N].copy()
                else:
                    vectors=directions[obs][split].copy()
                    if split=='test' and anchor!=4.:
                        seed=vectors[-1].copy()
                        transported=interp(anchor)@np.linalg.solve(interp(4.),seed)
                        vectors[-1]=transported/np.linalg.norm(transported)
                response=np.einsum('ab,tbc,nc->nta',H,propagator,vectors)
                sets[split]=(response[:,:len(HISTORY)],response[:,len(HISTORY):].reshape(len(vectors),-1))
            out[obs][anchor]=sets
    return out,prov,previous

if __name__=='__main__':
    ds,provenance,previous=make()
    evaluate(ds,'frozen',{'status':'AUTHENTICATED_FROZEN_TANGENT_PREFLIGHT_ONLY',
        'original_v18_24_sha256':provenance['v18_24_server_sha256'],
        'parent_proof_status':previous['status'],
        'model_free_at_calibration_and_prediction':True,
        'reference_generator':'CubicSpline interpolated authenticated 11D tangent cocycle; material 10D block'})
