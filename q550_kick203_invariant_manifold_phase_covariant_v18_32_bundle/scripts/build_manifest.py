#!/usr/bin/env python3
"""SHA manifest excluding live logs, ephemeral runtime and .pyc caches."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];out={}
for p in R.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '/__pycache__/' in '/'+rel or rel.endswith(('.pyc','.log','.tmp','~')):continue
    out[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=dict(sorted(out.items()))),indent=2)+'\n')
print('V18_32_SHA256_ENTRIES',len(out))
