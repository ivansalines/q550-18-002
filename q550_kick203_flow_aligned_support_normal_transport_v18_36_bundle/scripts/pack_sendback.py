#!/usr/bin/env python3
"""Fail closed on absent new original Q550 normal transport proof."""
import json,zipfile,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'results/original_v18_36_proof.json'
if not p.is_file():raise RuntimeError('Missing ORIGINAL v18.36 Q550 run; preflight is not a certificate')
j=json.loads(p.read_text())
if (j.get('status')!='ORIGINAL_Q550_FLOW_ALIGNED_SUPPORT_NORMAL_TRANSPORT_COMPLETED' or j.get('original_integrations')!=13 or j.get('case_count')!=12 or not j.get('all_seeds_jointly_admissible') or not j.get('original_ode_sha256_verified') or not j.get('includes_original_jacobian_cotangent_transport') or not j.get('checks_transport_against_frozen_candidate_gradient') or not j.get('no_physical_material_manifold_certified')):
    raise RuntimeError('Incomplete/incorrect v18.36 server proof')
for f in ('original_v18_36_normal_profiles.csv','original_v18_36_joint_support_cases.csv','original_v18_36_seed_attempts.csv','original_v18_36_normal_transport.png'):
    if not (R/'results'/f).is_file():raise RuntimeError('Missing original v18.36 file: '+f)
files=json.loads((R/'SHA256SUMS_OUTPUT.json').read_text())['files']
for n,h in files.items():
    if not (R/n).is_file() or hashlib.sha256((R/n).read_bytes()).hexdigest()!=h:raise RuntimeError('Manifest failure '+n)
out=R.parent/(R.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for n in sorted(files):z.write(R/n,R.name+'/'+n,compress_type=zipfile.ZIP_STORED if n.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'SHA256SUMS_OUTPUT.json',R.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(out) as z:
    if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={R.name}:raise RuntimeError('Bad final sendback ZIP')
print('SEND_BACK',out)
