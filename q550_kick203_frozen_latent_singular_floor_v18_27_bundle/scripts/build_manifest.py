"""Deterministic content hash excluding changing logs and temporary parent extraction."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
out={}
for p in ROOT.rglob('*'):
    if not p.is_file():continue
    relative=p.relative_to(ROOT).as_posix()
    if relative=='SHA256SUMS_OUTPUT.json' or relative.startswith('.runtime/') or '__pycache__/' in relative or p.suffix in {'.pyc','.log','.tmp'}:continue
    out[relative]=hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'algorithm':'SHA256','files':dict(sorted(out.items()))},indent=2)+'\n')
print('v18.27 immutable SHA256 entries:',len(out))
