#!/usr/bin/env python3
"""Fail closed: package only after original Q550 micro-time run and graph."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];res=R/'results';p=res/'original_v18_35_proof.json'
if not p.is_file():raise RuntimeError('Missing real v18.35 Q550 original proof; preflight is insufficient')
j=json.loads(p.read_text())
if (j.get('version')!='v18.35' or j.get('status')!='ORIGINAL_Q550_NEAR_SURFACE_MOVING_FRAME_AND_DEFECT_BUDGET_COMPLETED'
    or j.get('original_ode_input_sha256_verified') is not True or j.get('original_ode_integrations')!=15
    or j.get('case_count')!=12 or j.get('first_exit_diagnostics')!=120 or j.get('micro_sample_count',0)<1800
    or not j.get('original_v18_34_seed_reproduction') or not j.get('no_physical_invariant_manifold_certified')
    or not j.get('calibration_uses_training_only') or not j.get('if_outside_at_start_no_exit_claim')):
    raise RuntimeError('Incomplete/misrepresented v18.35 original Q550 certificate')
for name in ('original_v18_35_first_exits.csv','original_v18_35_microprofiles.csv','original_v18_35_case_summary.csv',
             'original_v18_35_moving_frame_microdefect.png'):
    if not (res/name).is_file():raise RuntimeError('Missing original result '+name)
files=json.loads((R/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,h in files.items():
    if not (R/name).is_file() or hashlib.sha256((R/name).read_bytes()).hexdigest()!=h:
        raise RuntimeError('Manifest mismatch '+name)
out=R.parent/(R.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for name in sorted(files):z.write(R/name,R.name+'/'+name,compress_type=zipfile.ZIP_STORED if name.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'SHA256SUMS_OUTPUT.json',R.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(out) as z:
    if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={R.name}:
        raise RuntimeError('New sendback ZIP CRC/root verification failed')
print('SEND_BACK',out)
