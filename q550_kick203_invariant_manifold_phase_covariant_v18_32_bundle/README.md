# Q550 v18.32 — Invariant-Manifold Tangency & Phase-Covariant Constraint Audit

## Scientific question

Does the original Q550 vector field admit **phase-covariant invariant hypersurface candidates** that remain tangent to the dynamics across independent postures, phase offsets and transverse states? This differs fundamentally from v18.31's search for *first integrals*.

A local equation `C(x, theta) = 0` can define a forward-invariant hypersurface if, in an open neighborhood,

\[
\mathcal L_F C = \nabla_x C\cdot F_x+\partial_\theta C\,F_\theta=\mu(\theta)\,C.
\]

Unlike a first integral, this does not require `C` to be conserved away from the zero-level surface. Conversely, arbitrary local flow-box coordinates can generate invariant surfaces. **A numerically passing candidate is therefore not a privileged physical material constraint**. The study is a local diagnostic and does **not** test global recurrence/closure.

## Input provenance

- `inputs/v18_31_original_server_sendback.zip` is an unmodified, SHA256-verified original server archive, including v18.31.2 recovery results and its entire recursively nested executable genealogy.
- v18.31 original proof reports **0 survived first-integral candidates** in the tested degree-2 material-polynomial dictionary. That negative result must not be overstated to exclude invariant manifolds.
- The new `checkpoint_io_v18_32.py` verifies the 67 v18.31 archive members against the original manifest, the original proof status, and the embedded SHA-pinned v18.30 ancestor. Original Q550 model dependencies are also SHA-pinned against `reference/q550_state_impulse_response_v13.py`. The adapted copy of `checkpoint_io_v18_31.py` changes only its local path / hash selection to load the nested old ZIP from `.runtime`; the authentic historical copy remains in the parent archive.
- Original Q550 ODE is loaded on the server from `/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle`. It is not replaced by a surrogate. First ten state variables are material, last is the phase clock.

## Preregistered candidate dictionary

Using `x_i=(y_i-center_i)/scale_i` and `phi=theta-theta_ref`, test either phase-blind or phase-covariant dictionaries containing:

1. `x_i` (10 terms)
2. `x_i x_j` for `i <= j` (55 terms; degree 2 cases)
3. `x_i sin(phi)` and `x_i cos(phi)` (20 terms; phase-covariant cases)

There are **no clock-only terms** and no independent constant feature. This eliminates one easy source of purely clock-generated pseudo-constraints but does not eliminate all artificial flow-box constructions. The dictionary is not invariant under arbitrary material coordinate transformations.

For each dictionary, use `mu(theta) = lambda + mod*sin(phi)`, with `lambda ∈ {-1, -0.5, 0, 0.5, 1}` and `mod ∈ {0}` for phase-blind or `{0, -0.3, 0.3}` for phase-covariant. Total: **40 candidate fits**.

Whiten feature columns before SVD; add an explicit penalty for nonzero C at the seven original orbit anchors. Select **the top two candidates per dictionary family using training objective only** (four total). Holdout scores are reported, not used to tune coefficients, cofactor choices, or choose the finalists.

## Holdout and geometric tests

- Anchors: `xi = [3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75]`.
- Training: 392 independent off-trajectory material/phase states, with declared perturbation levels and RNG seed 1832.
- Holdout: 224 separate states, larger transverse perturbations and different phase widths, RNG seed 1909.
- Check `L_F C - mu C` **at all holdout states** and separately at each of the seven postures.
- Shift phase of an additional independent holdout subsample by `-0.6` and `+0.6` radians, recomputing the actual original Q550 field, not reusing stale derivatives.
- Project an independent sparse holdout group onto `C=0` by declared normalized-coordinate Euclidean projection, check original-field tangency `L_F C` at projected points and integrate up to six such points over `0.25 xi` to inspect drift.
- **Numerical candidate screen** requires holdout Lie/cofactor residual, normalized on-surface tangency, transported level-set drift, anchor proximity, and phase-shifted residual each below `1e-6`. The diagnostic projection metric is not a physical material metric.
- If a candidate fails, retain its complete diagnostics but **do not claim an invariant manifold**. If a candidate passes, label it `NUMERICAL_LOCAL_HYPERSURFACE_CANDIDATE_NOT_PHYSICAL`; no physical constraint certificate is issued either way.
- The Q550 is not assumed to possess a first integral, an invariant manifold, a globally closed material surface, constitutive memory, or intrinsic torsion.

## Execute on original Linux server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_invariant_manifold_phase_covariant_v18_32_bundle.zip
cd q550_kick203_invariant_manifold_phase_covariant_v18_32_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_32_server.log
```

For a nonstandard model root:

```bash
bash scripts/run_on_server.sh --base-root /absolute/path/to/pinned/q550/model
```

The server script performs 11 synthetic mathematical tests, authenticates the prior original server archive, integrates the Q550 anchor trajectory once, evaluates the original field on the sampled states, fits the 40 candidate equations, carries out short independent holdout flows on fitted surfaces, produces a figure and packages the reproducible sendback. It does not regenerate the full 400-orbit trajectory. Original server runtimes can vary depending on the original ODE evaluation cost.

Output:

`/root/elab1/hysteresis/q550_kick203_invariant_manifold_phase_covariant_v18_32_sendback.zip`

### Offline preflight (no original Q550 run)

```bash
bash scripts/run_preflight.sh
```

This verifies the authentic parent, loader, checkpoint, and method tests, but **does not** create a Q550 scientific result. `scripts/pack_sendback.py` refuses to certify preflight-only output.

## Results

- `results/frozen_preflight_v18_32.json`: ancestor authentication only.
- `results/original_invariant_manifold_proof_v18_32.json`: original server experiment, 40 training selections, 4 held-out candidate tests, phase shifts, projected tangency, drift, and conservative status.
- `results/original_manifold_candidates_v18_32.json`: fitted coefficients, exact center and coordinate scales, phase anchor.
- `results/original_manifold_posture_transfer_v18_32.csv`: seven-posture comparison for each finalist.
- `results/original_manifold_transfer_v18_32.png`: plot of held-out residual by posture.
- `scripts/manifold_math_v18_32.py`: executable equations and projections with synthetic regression tests in `tests/test_manifold_v18_32.py`.
- `SHA256SUMS_OUTPUT.json`: manifest excluding live logs and `.runtime`.

## Interpretation boundaries

No discovered surface is certified as a physical constraint. A general exact local invariant surface can follow from flow-box coordinates without an intrinsic constitutive geometric restriction. Stronger conclusions would require physically derived admissibility conditions, a privileged physical metric/domain, tests over global returns and overlaps, or rigorous interval bounds. This audit tests only a finite dictionary and finite sampled Q550 neighborhood, and cannot prove global nonexistence when all candidates fail.

All documentation and Python source comments are in English.
