"""SHA256 immutable bundle files; never include active logs or runtime caches."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files={}
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(ROOT).as_posix()
 if rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '__pycache__/' in rel or p.suffix in {'.pyc','.log','.tmp'}:continue
 files[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'algorithm':'SHA256','files':dict(sorted(files.items()))},indent=2)+'\n')
print('v18.28 SHA256 immutable entries',len(files))
