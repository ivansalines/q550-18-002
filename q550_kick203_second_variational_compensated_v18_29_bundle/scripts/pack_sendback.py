#!/usr/bin/env python3
"""Fail closed unless authentic original Q550 compensated pairs were executed."""
import csv,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
proof=R/'original_compensated_proof_v18_29.json'
if not proof.is_file():raise RuntimeError('Server Q550 original compensated proof absent; preflight cannot masquerade as server sendback')
status=json.loads(proof.read_text())
if status.get('status')!='ORIGINAL_Q550_COMPENSATED_PAIR_SECOND_VARIATIONAL_CONVERGENCE_COMPLETED':
 raise RuntimeError('Incomplete Q550 original v18.29 proof')
if status.get('pair_comparisons')!=6 or status.get('case_count')!=2 or status.get('original_integrations',0)<20:
 raise RuntimeError('Incomplete Q550 original comparisons')
if not status.get('original_source_SHA256_verified') or not status.get('legacy_pair_response_not_used_in_compensated_integration'):
 raise RuntimeError('Insufficient Q550 provenance or leaked old pair data into compensated solver')
required=['original_compensated_pairs_v18_29.csv','original_compensated_profiles_v18_29.csv',
 'original_jacobian_source_v18_29.csv','original_compensated_floor_comparison_v18_29.png',
 'original_compensated_profile_v18_29.png']
for name in required:
 if not (R/name).exists():raise RuntimeError('Missing original-Q550 output '+name)
if len(list(csv.DictReader((R/required[0]).open())))!=6:raise RuntimeError('Six-case audit incomplete')
manifest=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,sha in manifest.items():
 file=ROOT/name
 if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=sha:
  raise RuntimeError('Manifest mismatch '+name)
target=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
 for rel in sorted(manifest):
  z.write(ROOT/rel,ROOT.name+'/'+rel,compress_type=(zipfile.ZIP_STORED if rel.endswith('.zip') else zipfile.ZIP_DEFLATED))
 z.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(target) as z:
 if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={ROOT.name}:
  raise RuntimeError('Packaged sendback failed ZIP-root/CRC validation')
print('SEND_BACK',target)
