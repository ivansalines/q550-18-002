# Q550 v18.35 — Near-Surface Boundary Layer & Local Transport Validity Audit

**Status in distributed bundle:** Authenticated-parent preflight only. Original Q550 v18.35 nonlinear integration has **not** been run on this machine. The only way to generate a `sendback` is to run the pinned Q550 ODE on the original server.

## Scientific question

v18.34 sampled the defect every 0.0125 xi and observed an enormous *fixed-start* diagnostic material distance (>450 normalized units at the first post-start sample). That does **not** prove that the evolving perturbation left a local *co-moving* tube; it also does **not** show the state was initially inside any defined calibration region. v18.35 resolves the first 0.0125 xi and distinguishes these issues.

The **two original fitted v18.33 surfaces** and their coefficients are frozen. No selection, refitting, or held-out future information is used to choose them:

- `phasecov_d2_lam-1.00_mod+0.00`
- `phaseblind_d2_lam-1.00_mod+0.00`

For each surface, replay original v18.34 projected holdout seeds at anchors xi=3.5, 4.0, 4.5 (two seeds each; 12 cases). Reproduce the genuine previous C endpoint at delta-xi=0.0125 and abort if it disagrees.

## Measurements

The micro-time grid has 171 distinct nodes, log-refined down to 1e-10 xi, and resolves delta-xi in `[0,0.0125]` only. Each pair uses an augmented DOP853 integration of:

1. The projected holdout seed, initially on fitted `C=0`;
2. A **phase-aligned reference** with the original central material coordinates but the same clock phase as the projected seed; this is an auxiliary Q550 solution, not the original central orbit if the clocks differ;
3. An integrated cofactor-source ledger `Z' = exp(-mu t) [L_F C - mu C]`, with constant `mu=-1`, giving `D(t)=exp(mu*t)*Z(t)`.

At each time node save:

- Signed source `r = L_F C - mu C`, observed `C(t)-exp(mu*t) C(0)`, integral budget and closure error;
- Material distance from the **fixed projected seed** and from the **phase-aligned moving reference** (same specified diagnostic scaling as v18.33);
- Nearest distance to the *local actual calibration training sample cloud* (56 points), plus the moving-ball distances using the fixed 95th-percentile and maximum local training radii;
- Initial clock offset from the original central anchor and whether it falls inside the training phase band `|delta theta| <= 0.25` rad;
- The joint **diagnostic** support flag: moving material distance within the local training radius **and** phase offset within the training band. This is a conservative extrapolation to a moving ball, **not** a mathematical guarantee of training data coverage or a physical constraint;
- Bracketed/refined first outward crossings for five material-distance thresholds in both frames. A trajectory outside from t=0 is reported as `OUTSIDE_AT_START`, **never as an exit**. `NO_EXIT_OBSERVED` is also possible.

Two selected cases have a second, tighter DOP853 solve to audit precision sensitivity. The exact cofactor defect identity is algebraic; its closure tests the integration, not candidate invariance.

## Limitations and interpretation

The material normalization from the original 7 anchors is not a physically privileged metric. The phase-aligned moving reference is chosen diagnostically. Training support is a finite, anisotropic cloud in 10 material coordinates and forcing phase; a radius bound alone is not equivalent to set membership. A candidate surface may have a nonzero source immediately at t=0 even if `C(0)=0`; that is a local tangency failure, not proof of an intrinsic material flip. No material first integral, physically admissible constraint manifold, certified normal curvature, or Poincare return has been established.

## Full execution on Q550 original server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_near_surface_boundary_layer_v18_35_bundle.zip
cd q550_kick203_near_surface_boundary_layer_v18_35_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_35_server.log
```

Output ZIP, created one directory above extracted bundle:
`/root/elab1/hysteresis/q550_kick203_near_surface_boundary_layer_v18_35_sendback.zip`.

Original SHA-pinned Q550 ODE modules must be available at `/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle` or pass `--base-root` to `scripts/run_on_server.sh`. The run fails if any pinned source file differs.

## Offline integrity preflight (no original ODE integration)

```bash
bash scripts/run_preflight.sh
```

It authenticates all members of the genuine v18.34 sendback and checks the immutable v18.33 candidates nested within its genealogy. `scripts/pack_sendback.py` refuses to package the preflight as a completed original experiment.

## Output files after original Q550 run

- `results/original_v18_35_microprofiles.csv` — original fields, co-moving/fixed distances and integrated defect, 12 cases x 171 nodes;
- `results/original_v18_35_first_exits.csv` — 120 threshold diagnostics, explicitly representing `OUTSIDE_AT_START`;
- `results/original_v18_35_case_summary.csv` — independent case summary, support and initial tangency;
- `results/original_v18_35_moving_frame_microdefect.png` — two-panel comparison;
- `results/original_v18_35_proof.json` — original-run status, replay and accuracy checks;
- `SHA256SUMS_OUTPUT.json` — SHA256 for scripts, results, immutable parent, tests and documentation;
- Original parent full sendback ZIP in `inputs/`, preserving all prior executable genealogy.

## Dependency notes

Python 3.13 preferred; NumPy, SciPy, Matplotlib; pinned Q550 ODE source files authenticated at runtime. No external network or file download. Comments and documentation in English. Active `*.log`, temporary files, `__pycache__` and `.runtime/` files are excluded from sendback hashes and packaging. All ZIP contents are under exactly one top-level directory.
