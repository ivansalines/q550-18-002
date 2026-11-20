#!/usr/bin/env python3
"""SHA256 reproducibility inventory excluding active logs and runtime."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];files={}
for p in sorted(R.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if (rel=='SHA256SUMS_OUTPUT.json' or rel.startswith('.runtime/') or '/__pycache__/' in '/'+rel
        or rel.endswith(('.pyc','.log','.tmp','~'))):continue
    files[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'SHA256SUMS_OUTPUT.json').write_text(json.dumps(dict(algorithm='SHA256',files=files),indent=2)+'\n')
print('V18_35_SHA256_ENTRIES',len(files))
