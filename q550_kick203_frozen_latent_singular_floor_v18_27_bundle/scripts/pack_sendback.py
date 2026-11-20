"""Refuse preflight-only claims; immutable SHA256 verification and clean root."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
proof=R/'original_high_precision_floor_proof_v18_27.json'
if not proof.exists():raise RuntimeError('No original ODE floor proof: preflight-only cannot be packaged')
status=json.loads(proof.read_text())
if status.get('status')!='ORIGINAL_Q550_HIGH_PRECISION_NUMERICAL_FLOOR_SCAN_COMPLETED':
    raise RuntimeError('Original-Q550 status is missing')
if status.get('rows')!=45 or status.get('new_original_ode_integrations')!=272:
    raise RuntimeError('Full 45-row / 272-solve audit not complete')
for f in ['original_tight_floor_comparison_v18_27.csv','original_subspace_summary_v18_27.json',
          'original_principal_subspace_v18_27.csv','original_latent_bases_v18_27.npz']:
    if not (R/f).exists():raise RuntimeError('Missing '+f)
ledger=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for file,digest in ledger.items():
    if hashlib.sha256((ROOT/file).read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Checksum mismatch: '+file)
target=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
    for file in sorted(ledger):
        z.write(ROOT/file,ROOT.name+'/'+file,
                compress_type=zipfile.ZIP_STORED if Path(file).suffix=='.zip' else zipfile.ZIP_DEFLATED)
    z.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(target) as z:
    if z.testzip():raise RuntimeError('Corrupted sendback ZIP')
    if {n.split('/')[0] for n in z.namelist()}!={ROOT.name}:raise RuntimeError('Unexpected ZIP root')
print('SEND_BACK',target)
