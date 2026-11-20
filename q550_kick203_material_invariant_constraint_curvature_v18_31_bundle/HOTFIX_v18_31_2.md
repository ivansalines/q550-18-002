# Q550 v18.31.2 — NumPy JSON and verified partial-run recovery hotfix

The server completed the original Q550 candidate and optional conditional-curvature work,
then failed at `json.dumps(report)` because the report contained an `np.bool_` value.
`numpy.bool_` is not JSON-native, even though ordinary Python `bool` is.
The previous v18.31.1 checkpoint-slope correction is retained.

This overlay fixes NumPy boolean, integer, float and array serialization in the final
original-Q550 proof and adds a controlled recovery path for a *specific* failure:
all three original intermediates were written before the final JSON serialization crash.

On re-run, if all three intermediates exist and the proof does not:
- reauthenticates the original v18.30 input archive and original pinned Q550 code;
- replays the single baseline anchor orbit and the deterministic 392/224 sampled fields;
- reconstructs singular spectra and verifies candidate ranks, scores, and decisions
  against the CSV left by the prior full run;
- checks any surviving coefficient vectors and conditional-curvature outputs;
- reconstitutes the final original proof with explicit recovery metadata;
- generates the original diagnostic plot, a fresh SHA256 manifest, and the sendback ZIP.

It deliberately does **not** repeat expensive independent conservation flows or
conditional curvature integrations already completed before the serialization crash.
It refuses recovery if any intermediate is absent or inconsistent. In that case, run
`python3.13 scripts/original_material_invariants_v18_31.py` to recompute.

## Overlay from the hysteresis parent directory

```bash
cd /root/elab1/hysteresis
unzip -o q550_v18_31_2_json_bool_recovery_hotfix.zip
cd q550_kick203_material_invariant_constraint_curvature_v18_31_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_31_server_retry_2.log
```

When complete, send back
`/root/elab1/hysteresis/q550_kick203_material_invariant_constraint_curvature_v18_31_sendback.zip`.

All source comments and documentation are in English. The original ODE, inputs, source
hashes, scientific selection thresholds, and interpretation flags are unchanged.
