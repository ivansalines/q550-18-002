"""Do not package a preflight-only bundle as an original nonlinear experiment."""
import hashlib,json,zipfile,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
p=R/'original_second_variational_proof_v18_28.json'
if not p.exists():raise RuntimeError('No genuine ORIGINAL_Q550 second-variational proof: server not run')
z=json.loads(p.read_text())
if z.get('status')!='ORIGINAL_Q550_SECOND_VARIATIONAL_SOURCE_AND_NONLINEAR_PAIR_AUDIT_COMPLETED':
 raise RuntimeError('Original Q550 proof incomplete')
if z.get('number_of_cases')!=4 or z.get('epsilon_pairs')!=8 or z.get('new_original_ode_integrations',0)<40:
 raise RuntimeError('Incomplete second variation or independent +/- nonlinear comparisons')
if not z.get('source_verified_against_pin') or not z.get('phase_common_within_pair'):
 raise RuntimeError('Original source or phase check absent')
for name in ['original_second_variational_pairs_v18_28.csv','original_second_variational_profiles_v18_28.csv',
             'original_second_variational_sources_v18_28.csv','original_second_variational_vs_pairs_v18_28.png']:
 if not (R/name).exists():raise RuntimeError('Missing original result '+name)
manifest=json.loads((ROOT/'SHA256SUMS_OUTPUT.json').read_text())['files']
for file,sha in manifest.items():
 if hashlib.sha256((ROOT/file).read_bytes()).hexdigest()!=sha:
    raise RuntimeError('Manifest SHA mismatch '+file)
path=ROOT.parent/(ROOT.name.replace('_bundle','_sendback')+'.zip')
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5,allowZip64=True) as archive:
 for rel in sorted(manifest):
    archive.write(ROOT/rel,ROOT.name+'/'+rel,compress_type=zipfile.ZIP_STORED if rel.endswith('.zip') else zipfile.ZIP_DEFLATED)
 archive.write(ROOT/'SHA256SUMS_OUTPUT.json',ROOT.name+'/SHA256SUMS_OUTPUT.json')
with zipfile.ZipFile(path) as check:
 if check.testzip() or {r.split('/')[0] for r in check.namelist()}!={ROOT.name}:
    raise RuntimeError('Broken final sendback archive')
print('SEND_BACK',path)
