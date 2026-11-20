"""Package original-nonlinear-only v18.25, excluding live logs and runtime."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
proof=ROOT/'results/original_ode_transport_proof.json'
if not proof.exists() or json.loads(proof.read_text()).get('status')!='ORIGINAL_Q550_NONLINEAR_PAIRED_DELAY_FRAME_TRANSPORT_COMPLETED':
    raise RuntimeError('Frozen preflight alone cannot be certified as original nonlinear v18.25')
for name in ('original_transport_comparison.csv','original_calibration_diagnostics.csv','original_summary.json'):
    if not (ROOT/'results'/name).exists():raise RuntimeError('Missing original server result '+name)
sums=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for rel,sha in sums.items():
    if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=sha:raise RuntimeError('Input/result SHA mismatch '+rel)
output=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
    for rel in sorted(sums):
        f=ROOT/rel
        z.write(f,arcname=ROOT.name+'/'+rel,compress_type=zipfile.ZIP_STORED if f.suffix=='.zip' else zipfile.ZIP_DEFLATED)
    z.write(ROOT/'SHA256SUMS_OUTPUT.json',arcname=ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(output) as z:
    if z.testzip():raise RuntimeError('ZIP CRC failure')
    if {n.split('/')[0] for n in z.namelist()}!={ROOT.name}:raise RuntimeError('Bad sendback root')
print('SEND_BACK',output)
