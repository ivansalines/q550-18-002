# Q550 v18.31 — Material Invariant Discovery & Constraint-Normal Curvature Audit

## Question

Does the **SHA-pinned original Q550 material vector field** possess simple low-degree conserved scalar quantities near kick 203 that could serve as legitimate geometric constraints? If such a candidate survives independent transverse tests, what would its **conditional** normal curvature mean? No assumed material invariant is silently introduced.

This audit deliberately separates:

1. **Known clock/gauge**: common phase variation is zero, but the phase coordinate itself evolves. An approximately constant phase rate is **not** a material first integral.
2. **Empirical invariant discovery**: search constant-coefficient material polynomials of degrees 1 and 2, using vector-field Lie derivatives over many transversely perturbed states at seven anchors.
3. **Out-of-sample discrimination**: different random transverse states, phase offsets, independent short Q550 trajectories, and stringent normalized derivative and drift thresholds. Merely flat behavior along one orbit **fails** this test.
4. **Conditional normal-curvature measurement**, only if a numerical candidate survives. A discovered approximate level set is **not** a certified physically admissible manifold.

An absence of candidates is a valid negative result **limited to the polynomial dictionary and sampled domain**; it is not a theorem that Q550 has no conservation laws.

## Original equation and mathematical protocol

The authentic Q550 11D source, Jacobian, baseline initial state, time scale and source hashes are unchanged and inherited through the original v18.30 server sendback. The first ten coordinates are the material state; the last is the phase clock.

For normalized material coordinates \(x_i=(y_i-c_i)/s_i\), discover coefficients \(q\) for

\[
C_q(y)=\sum_i q_i x_i + \sum_{i\le j}q_{ij}x_i x_j.
\]

Build training matrix rows \(\nabla C_q\cdot F\), perform column-normalized SVD, and screen its smallest right singular vectors. A real first integral must have \(D C\cdot F=0\) over an open neighborhood, **not simply on one trajectory**. The training search and transverse holdouts are independently seeded and have different amplitudes and phase ranges. Candidates must pass both stringent relative Lie-derivative tests and independent flow-drift tests. The full singular spectra, candidate coefficients, thresholds, normalization, and rejected candidates are logged.

For any survivor, form \(G=DC\), \(K=D^2C\), project a diagnostic seed into \(\ker G\), and set the second-order normal jet \(w_0=-G^+ K[u,u]\). Then measure along the original Q550 second-variational flow:

\[
G u,\qquad G w+K[u,u],\qquad G F,\qquad \langle n,D^2F[u,u]\rangle.
\]

These are **conditional level-set diagnostics** only. Certification of an intrinsic physical constraint would additionally require derivation from the model, invariance of its actual physical domain and its compatibility with physically admissible perturbations. Even a tiny finite-time residual cannot supply that alone.

## Sample and scale policy

- Seven reference anchors: `3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75 xi`.
- 56 training and 32 holdout transverse field evaluations per anchor, plus anchor controls.
- Off-trajectory perturbations: separate RNG seeds, phase shifts, and test amplitudes larger than training.
- Ten linear features, or ten linear plus 55 quadratic (symmetric) features.
- Singular candidate prefilter threshold `2e-6`; strict acceptance derivative ratio `1e-7` on training and holdout, further trajectory drift ratio `1e-6`.
- One original DOP853 Q550 integration to build anchor states; additional independent validation integrations **only if** candidate invariants survive.
- Normalized coordinates and scale choices are recorded exactly to make the dictionary reproducible. This search is **not** gauge invariant under arbitrary nonlinear coordinate changes; its scope is explicitly finite.
- Original source evaluation exceptions in off-domain perturbations are tracked; too few finite points abort the audit.

## Integrity and genealogy

`inputs/v18_30_original_server_sendback.zip` is the **unaltered** SHA256-pinned, fully checked original Q550 server result (60 members). The v18.29/v18.28/etc. authentic genealogy is retained *inside it*, not reconstructed. All Python scripts, README, reference loader, input, test, outputs and hashes are included. The source ODE must still exist at the original pinned server location; no approximation substitutes for missing files.

Original Q550 model root (pinned against the reference script):

`/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle`

## Execution

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_material_invariant_constraint_curvature_v18_31_bundle.zip
cd q550_kick203_material_invariant_constraint_curvature_v18_31_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_31_server.log
```

Optional custom original source location (pinned source hashes must still match):

```bash
bash scripts/run_on_server.sh --base-root /absolute/path/to/pinned/original
```

Offline original archive authentication and synthetic tests, **no new Q550 server results**:

```bash
bash scripts/run_preflight.sh
```

## Outputs

- `results/frozen_preflight_v18_31.json`: genuine input proof and no-new-integration status.
- `results/original_invariant_discovery_proof_v18_31.json`: full singular spectra, clock diagnostics, all thresholds, transverse / held-out scores and qualitative limits.
- `results/original_invariant_candidates_v18_31.csv`: candidates and rejections.
- `results/original_discovered_candidate_coefficients_v18_31.json`: exact normalized coordinate center, scale and any surviving coefficient vector.
- `results/original_constraint_normal_curvature_v18_31.json`: **conditional** curvature, when numerically permissible; otherwise an explicit empty diagnostic.
- `results/original_invariant_singular_spectrum_v18_31.png`: relative spectra of invariant-discovery dictionaries.
- `SHA256SUMS_OUTPUT.json`: all immutable members; excludes running logs and `.runtime`.

Output sendback, generated **only after** genuine original-server results:

`/root/elab1/hysteresis/q550_kick203_material_invariant_constraint_curvature_v18_31_sendback.zip`

## Interpretation limits

A low singular value on one orbit does **not** imply conserved quantities. The off-trajectory holdout tests are essential; nevertheless even passed candidates are only numerical evidence. Phase-clock evolution is not a material invariant; coordinate changes can alter polynomial complexity. Without a physically derived conserved constraint, **no physical constraint-normal curvature is certified** and the off-constraint diagnostic impulses remain off-constraint. This audit does not prove physical torsion, a unique material metric, a global first integral, or autonomous memory.

All source comments and documentation are in English.
