"""SHA-checked sendback. Refuse preflight-only packages or active logs."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'results'
proof=RES/'original_ode_amplitude_proof.json'
if not proof.exists() or json.loads(proof.read_text()).get('status')!='ORIGINAL_Q550_NONLINEAR_VANISHING_AMPLITUDE_SCAN_COMPLETED':
    raise RuntimeError('Cannot certify v18.26 from frozen preflight alone')
for name in ('original_amplitude_prediction.csv','original_rank20_vs_10.csv',
             'original_even_odd_probe.csv','original_reduced_dataset_v18_26.npz','original_summary.json'):
    if not (RES/name).exists():raise RuntimeError('Missing independent original nonlinear output '+name)
manifest=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for name,sha in manifest.items():
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:
        raise RuntimeError('SHA256 mismatch '+name)
output=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as z:
    for name in sorted(manifest):
        file=ROOT/name
        z.write(file,arcname=ROOT.name+'/'+name,
            compress_type=zipfile.ZIP_STORED if file.suffix=='.zip' else zipfile.ZIP_DEFLATED)
    z.write(ROOT/'SHA256SUMS_OUTPUT.json',arcname=ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(output) as z:
    if z.testzip():raise RuntimeError('Bad sendback ZIP CRC')
    if {name.split('/')[0] for name in z.namelist()}!={ROOT.name}:
        raise RuntimeError('Wrong sendback root')
print('SEND_BACK',output)
