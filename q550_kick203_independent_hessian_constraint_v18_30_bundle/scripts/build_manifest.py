#!/usr/bin/env python3
"""Rebuild immutable SHA256 inventory; exclude all active tee logs and runtime caches."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files={}
for file in ROOT.rglob('*'):
 if not file.is_file():continue
 rel=file.relative_to(ROOT).as_posix()
 if rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '__pycache__/' in rel or file.suffix in ('.pyc','.log','.tmp') or rel.endswith('~'):
  continue
 files[rel]=hashlib.sha256(file.read_bytes()).hexdigest()
(ROOT/'SHA256SUMS_OUTPUT.json').write_text(json.dumps({'algorithm':'SHA256','files':dict(sorted(files.items()))},indent=2)+'\n')
print('v18.30 SHA256 entries',len(files))
