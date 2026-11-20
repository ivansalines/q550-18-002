# v18.31.1 — Q550 checkpoint-tier slope loading hotfix

## Incident

The server correctly completed all synthetic tests and authenticated v18.30, but
`original_material_invariants_v18_31.py` attempted to retrieve `slope` from the
outer checkpoint dictionary and raised `KeyError: 'slope'`.

The authenticated v18.7/v18.6 loader returns `{standard: {...}, tight: {...}}`;
`source_state_11D` and `slope` are stored *inside each tolerance tier*.

## Change

`original_material_invariants_v18_31.py` now selects and validates the `tight`
checkpoint before accessing the source state and slope. The new regression test
covers correct selection and malformed checkpoint rejection. No field equations,
model parameters, perturbations, candidate thresholds, invariant calculations,
original Q550 input files, or historical genealogy are changed.

The independently authenticated `tight` checkpoint has:

- `slope = 0.1343837359721647`
- `source_state_11D.shape = (11,)`

## Installation on the existing server tree

```bash
cd /root/elab1/hysteresis
unzip -o q550_v18_31_1_checkpoint_slope_hotfix.zip
cd q550_kick203_material_invariant_constraint_curvature_v18_31_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_31_server_retry.log
```

The patch archive preserves the exact v18.31 directory root, includes the
patched source and test plus this note and an updated SHA256 manifest. The runner
regenerates the manifest after the original-Q550 run. The archive cannot package
a completed original Q550 result unless the scientific proof files exist.

## Validation scope

The authenticated *original checkpoint loader* and all ten local regression tests
were run successfully; the original 11D nonlinear Q550 server execution remains
to be performed on the user's server. Do not equate this hotfix with an original
material-invariant result.
