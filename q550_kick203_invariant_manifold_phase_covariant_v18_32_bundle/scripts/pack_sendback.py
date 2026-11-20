#!/usr/bin/env python3
"""Fail closed: never issue an original Q550 sendback from the preflight."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
proof_path=R/'original_invariant_manifold_proof_v18_32.json'
if not proof_path.is_file():raise RuntimeError('Original Q550 manifold proof absent: preflight not sufficient')
p=json.loads(proof_path.read_text())
if (p.get('status')!='ORIGINAL_Q550_PHASE_COVARIANT_MANIFOLD_DIAGNOSTIC_COMPLETED'
    or not p.get('original_ODE_source_SHA256_verified') or p.get('original_ode_integrations',0)<1
    or p.get('train_states')!=392 or p.get('holdout_states')!=224):
    raise RuntimeError('Original Q550 audit incomplete')
for name in ('original_manifold_candidates_v18_32.json','original_manifold_posture_transfer_v18_32.csv','original_manifold_transfer_v18_32.png'):
    if not (R/name).is_file():raise RuntimeError('Missing server result '+name)
manifest=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for path,digest in manifest.items():
    f=ROOT/path
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise RuntimeError('SHA mismatch '+path)
out=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4,allowZip64=True) as z:
    for p in sorted(manifest):z.write(ROOT/p,ROOT.name+'/'+p,compress_type=zipfile.ZIP_STORED if p.endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(out) as z:
    if z.testzip() or {p.split('/')[0] for p in z.namelist()}!={ROOT.name}:raise RuntimeError('Broken ZIP root/CRC')
print('SEND_BACK',out)
