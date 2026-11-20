#!/usr/bin/env python3
"""Fail closed: original Q550 results and verified parent required before sendback."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];r=R/'results'
p=r/'original_v18_33_proof.json'
if not p.is_file():raise RuntimeError('v18.33 original Q550 results missing; preflight is not a server run')
j=json.loads(p.read_text())
if (j.get('status')!='ORIGINAL_Q550_COFACTOR_SELECTION_REPAIR_SURFACE_RETURN_COMPLETED'
    or j.get('original_ODE_source_SHA256_verified') is not True
    or j.get('candidate_grid_count')!=40 or j.get('train_states')!=392
    or j.get('holdout_states')!=224 or not j.get('no_holdout_in_selection')
    or not j.get('overlooked_phasecov_candidate_included')
    or j.get('original_ode_integrations',0)<1):
    raise RuntimeError('Incomplete/unauthenticated v18.33 original result')
for name in ('original_v18_33_selection_scan.csv','original_v18_33_surface_retests.json',
    'original_v18_33_posture_overlap.csv','original_v18_33_clock_return.csv',
    'original_v18_33_selection_vs_holdout.png','original_v18_33_surface_return.png'):
    if not (r/name).is_file():raise RuntimeError('Missing original v18.33 output '+name)
manifest=json.loads((R/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,sha in manifest.items():
    f=R/name
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise RuntimeError('Manifest mismatch '+name)
output=R.parent/(R.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for name in sorted(manifest):
        z.write(R/name,R.name+'/'+name,compress_type=zipfile.ZIP_STORED if name.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'SHA256SUMS_OUTPUT.json',R.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(output) as z:
    if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={R.name}:raise RuntimeError('Bad ZIP root or CRC')
print('SEND_BACK',output)
