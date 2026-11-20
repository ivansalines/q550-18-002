#!/usr/bin/env python3
"""SHA256 list excluding running logs, cached runtime, and transient files."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
files={}
for f in ROOT.rglob('*'):
    if not f.is_file():continue
    rel=f.relative_to(ROOT).as_posix()
    if rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '__pycache__/' in rel or f.suffix in ('.pyc','.log','.tmp') or rel.endswith('~'):continue
    files[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=dict(sorted(files.items()))),indent=2)+'\n')
print('v18.31 SHA256 entries',len(files))
