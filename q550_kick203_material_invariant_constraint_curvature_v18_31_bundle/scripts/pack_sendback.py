#!/usr/bin/env python3
"""Fail closed without Q550 discovery and validated original source hashes."""
from pathlib import Path
import hashlib,json,csv,zipfile
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
path=R/'original_invariant_discovery_proof_v18_31.json'
if not path.is_file():raise RuntimeError('No original Q550 proof: a preflight cannot produce a sendback')
p=json.loads(path.read_text())
if p.get('status')!='ORIGINAL_Q550_MATERIAL_INVARIANT_DISCOVERY_AND_CONDITIONAL_CURVATURE_COMPLETED' or not p.get('pinned_original_ODE_SHA256_verified') or p.get('original_ode_integrations',0)<1 or p.get('train_states',0)<200 or p.get('holdout_states',0)<100:
    raise RuntimeError('Incomplete original Q550 material invariant discovery')
for name in ('original_invariant_candidates_v18_31.csv','original_constraint_normal_curvature_v18_31.json','original_discovered_candidate_coefficients_v18_31.json','original_invariant_singular_spectrum_v18_31.png'):
    if not (R/name).is_file():raise RuntimeError('Missing server result: '+name)
m=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for rel,expect in m.items():
    if not (ROOT/rel).is_file() or hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=expect:raise RuntimeError('SHA mismatch '+rel)
archive=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
    for rel in sorted(m):z.write(ROOT/rel,ROOT.name+'/'+rel,compress_type=zipfile.ZIP_STORED if rel.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(archive) as z:
    if z.testzip() or {x.split('/')[0] for x in z.namelist()}!={ROOT.name}:raise RuntimeError('Archive root or CRC failed')
print('SEND_BACK',archive)
