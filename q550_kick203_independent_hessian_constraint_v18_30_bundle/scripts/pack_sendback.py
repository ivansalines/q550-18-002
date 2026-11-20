#!/usr/bin/env python3
"""Fail closed unless the real original-Q550 v18.30 experiment was executed."""
from pathlib import Path
import csv,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
proof=R/'original_independent_hessian_proof_v18_30.json'
if not proof.is_file():raise RuntimeError('Original-Q550 v18.30 proof missing: preflight cannot manufacture server results')
d=json.loads(proof.read_text())
if d.get('status')!='ORIGINAL_Q550_INDEPENDENT_RHS_HESSIAN_DIAGNOSTIC_COMPLETED' or not d.get('original_ODE_input_SHA256_verified'):
 raise RuntimeError('Not an authenticated original-Q550 server Hessian audit')
if d.get('case_count')!=2 or d.get('case_summary_rows')!=4 or d.get('original_ode_integrations',0)<10:
 raise RuntimeError('Missing original Q550 integrations or audit rows')
required=['original_independent_hessian_summary_v18_30.csv','original_independent_hessian_source_v18_30.csv',
 'original_independent_hessian_profiles_v18_30.csv','original_rhs_vs_jac_hessian_v18_30.png',
 'original_constraint_hessian_even_profiles_v18_30.png']
for name in required:
 if not (R/name).is_file():raise RuntimeError('Missing server-only results '+name)
if len(list(csv.DictReader((R/required[0]).open())))!=4:raise RuntimeError('Incomplete cross-stencil comparison')
if len(list(csv.DictReader((R/required[1]).open())))<60:raise RuntimeError('Missing source samples')
manifest=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,exp in manifest.items():
 f=ROOT/name
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=exp:raise RuntimeError('Manifest mismatch '+name)
target=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
 for rel in sorted(manifest):
  z.write(ROOT/rel,ROOT.name+'/'+rel,compress_type=zipfile.ZIP_STORED if rel.endswith('.zip') else zipfile.ZIP_DEFLATED)
 z.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(target) as z:
 if z.testzip() or {n.split('/')[0] for n in z.namelist()}!={ROOT.name}:
  raise RuntimeError('Packaged ZIP root/CRC failure')
print('SEND_BACK',target)
