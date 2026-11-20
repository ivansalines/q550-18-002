"""Preflight on archived tangent data ONLY, not original nonlinear amplitudes.

All amplitudes produce the same normalized linear trajectory. The expected
lack of amplitude dependence under constant *normalized* noise is a necessary
sanity check. Fixed *absolute* noise must increase as epsilon shrinks.
"""
from pathlib import Path
import zipfile,json
import numpy as np
from scipy.interpolate import CubicSpline
from checkpoint_io_v18_26 import read
from checkpoint_io_v18_21 import PREFIX as PREFIX20
from frozen_preflight import observers
from blind_experiment import initial_directions,OBSERVERS
from blind_math import HISTORY,HORIZONS
from transport_math_v18_25 import ANCHORS,CAL_N
from amplitude_math_v18_26 import AMPLITUDES,evaluate,effective_sigma
ROOT=Path(__file__).resolve().parents[1]

def make(amplitudes=AMPLITUDES):
    data,provenance,proof=read();d=data['tight'];Hs=observers(d)
    with zipfile.ZipFile(ROOT/'.runtime/v18_20_original_server_sendback.zip') as z:
        records=json.loads(z.read(PREFIX20+'results/matched_hidden_seeds.json'))
    directions=initial_directions({r['name']:r['seed'] for r in records})
    xi=np.asarray(d['xi_nodes']);P=CubicSpline(xi,np.asarray(d['P_full11D'][:,:10,:10]),axis=0)
    baseline={obs:{} for obs in OBSERVERS}
    for anchor in ANCHORS:
        map_matrix=P(anchor+np.r_[HISTORY,HORIZONS])@np.linalg.inv(P(anchor))
        for obs in OBSERVERS:
            H=Hs[obs];parts={}
            for split in (('train','val','test') if anchor==4. else ('cal','test')):
                U=(directions[obs]['train'][:CAL_N] if split=='cal' else directions[obs][split].copy())
                if split=='test' and anchor!=4.:
                    U[-1]=P(anchor)@np.linalg.solve(P(4.),U[-1]);U[-1]/=np.linalg.norm(U[-1])
                values=np.einsum('ab,tbc,nc->nta',H,map_matrix,U)
                parts[split]=(values[:,:len(HISTORY)],values[:,len(HISTORY):].reshape(len(U),-1))
            baseline[obs][anchor]=parts
    return {float(e):baseline for e in amplitudes},provenance

if __name__=='__main__':
    ds,prov=make()
    summary=evaluate(ds,'frozen',{'status':'AUTHENTICATED_LINEAR_TANGENT_ONLY_NO_NEW_ODE_INTEGRATIONS',
                                  'parent_v18_25_sha256':prov['v18_25_server_sha256']},
                     amplitudes=AMPLITUDES,noise_modes=('none','fixed_normalized','fixed_absolute'))
    assert effective_sigma(AMPLITUDES[-1],'fixed_absolute')==0.01
    print('FROZEN PREFLIGHT',summary['rows'],'rows','amplitudes',AMPLITUDES)
