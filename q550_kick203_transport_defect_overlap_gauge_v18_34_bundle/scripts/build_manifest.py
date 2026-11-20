#!/usr/bin/env python3
"""SHA256 manifest excluding active server logs and runtime-extracted inputs."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];out={}
for p in sorted(R.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if (rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '/__pycache__/' in '/'+rel
        or rel.endswith(('.pyc','.log','.tmp','~'))):continue
    out[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=out),indent=2)+'\n')
print('V18_34_SHA256_ENTRIES',len(out))
