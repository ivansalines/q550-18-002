#!/usr/bin/env python3
"""Fail closed unless the authentic new Q550 defect-budget run is complete."""
from pathlib import Path
import json,hashlib,zipfile,csv
R=Path(__file__).resolve().parents[1];out=R/'results';p=out/'original_v18_34_proof.json'
if not p.exists():raise RuntimeError('Cannot package frozen preflight as original v18.34')
j=json.loads(p.read_text())
if (j.get('version')!='v18.34' or j.get('status')!='ORIGINAL_Q550_TRANSPORT_DEFECT_BUDGET_OVERLAP_GAUGE_COMPLETED'
    or j.get('original_ode_source_sha256_verified') is not True or j.get('original_ode_integrations')!=13
    or j.get('original_v18_33_endpoints_reproduced') is not True
    or j.get('total_sample_count',0)<900 or j.get('endpoint_count')!=36
    or j.get('no_certified_material_metric',False) is not True
    or j.get('no_material_constraint_certified',False) is not True):
    raise RuntimeError('Incomplete v18.34 original Q550 certification')
required=['original_v18_34_budget_samples.csv','original_v18_34_budget_segments.csv',
    'original_v18_34_budget_endpoints.csv','original_v18_34_overlap_gauge.csv',
    'original_v18_34_budget_closure_xi3p5_seed0.png','original_v18_34_source_profile.png',
    'original_v18_34_domain_exit.png']
for n in required:
    if not (out/n).is_file():raise RuntimeError('Missing original output '+n)
manifest=json.loads((R/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,sha in manifest.items():
    f=R/name
    if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise RuntimeError('SHA manifest mismatch '+name)
output=R.parent/(R.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for name in sorted(manifest):
        z.write(R/name,R.name+'/'+name,compress_type=zipfile.ZIP_STORED if name.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'SHA256SUMS_OUTPUT.json',R.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(output) as z:
    if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={R.name}:
        raise RuntimeError('Result archive failed CRC/root verification')
print('SEND_BACK',output)
