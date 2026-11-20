# Q550 v18.30 — Independent Hessian & Constraint-Tangent Curvature Audit

## Scientific purpose and scope

Compare two genuinely distinct **numerical constructions of the second directional derivative of the original Q550 vector field**:

1. **RHS-derived Hessian**: a fourth-order five-point directional second difference of the *pinned original* `support_rhs_float` vector field, with step sizes `h = 0.02` and `h = 0.08` in the normalized material direction.
2. **Jacobian-derived Hessian**: a fourth-order four-point derivative of the independently pinned original analytic Jacobian `float_support_jacobian`, evaluated at precisely the same `(y,u)` time samples and the same two step sizes.

Both witnesses share the same original ODE and source implementation; the comparison provides **numerical discrimination**, not an independent physical model. Neither finite-difference step agreement nor error between methods provides a certified interval error bound. Original Q550 RHS and Jacobian must pass pinned SHA256 checks on the server before integration.

Each second-order variational prediction satisfies

```
y' = F(y)
u' = J(y)u
w' = J(y)w + D²F(y)[u,u]
R_even(ε) = (ε/2) H w.
```

The `w` source is always computed from **RHS differences**, not from `D J`. Its entire observation time-profile is compared against the authenticated v18.29 Jacobian-derived predictions and separately compensated nonlinear pairs at `ε = 1e-5`, with the second variation then predicted at `ε = 1e-6`. The historical v18.29 profiles are read-only targets and **do not enter** the new variational RHS integration.

## Concrete scope

- `raw6`, anchor `xi = 4.5`: primary resolved signal from v18.29.
- `material3`, anchor `xi = 3.5`: weaker control to test numerical sensitivity.
- The very same archived matched 10D perturbation seeds, 10D observation matrices, nonlinear Q550 ODE, source state, phase and time scaling as v18.29.
- 17 past samples within `-0.5 xi` and three future horizons `+0.2, +0.5, +1.0 xi` (20 unique samples).
- Approximately **10 local original-Q550 ODE integrations** (two baseline integrations, two two-sided source-variational solves at each anchor). No 400-period orbit rebuild.
- Tight DOP853 baseline and variational tolerances `rtol=3e-13`, `atol=3e-14`, `max_step=0.015 xi`.
- The two source steps are checked for their absolute size relative to the actual material coordinates; this matters when some Q550 components are near zero.

## Constraint-tangent curvature: what is and is NOT known

The original v18.29 and its ancestors explicitly state that the diagnostic impulses were **OFF_CONSTRAINT_DIAGNOSTIC**. They do not provide a verified model-specific invariant manifold or material constraint function. Consequently **the default v18.30 run does not invent any physical constraint**. It checks that material variations share an exact phase-clock fiber (`δθ = 0`, `uθ = 0`, `wθ = 0`). This clock-fiber condition is **not** a model conserved quantity: the background phase evolves.

If and only if a **trusted, model-specific** Python module is supplied with `invariants(y)` mapping an 11D original-Q550 state to the conserved invariant vector, v18.30 additionally computes the constraint-tangent geometry:

```
G = D C(y)
G u = 0
G w + D²C(y)[u,u] = 0
u0 = projection of matched seed into ker(G_material)
w0 = - G_material^+ D²C(y0)[u0,u0]
```

Both derivatives of `C` are estimated numerically, **independently of the Q550 field source**, and their deviations are measured along the integrated original-Q550 trajectory. The module must be provided *explicitly* through `--constraints-module` and must be compatible with the actual Q550 conserved dynamics. If it is missing, no material constraint claim is made. If supplied but the invariant conservation checks fail, the result remains `DECLARED_INVARIANTS_NOT_VERIFIED`. A locally compatible supplied invariant is not automatically an interval-certified physical constraint; the report distinguishes these cases.

A constraint-adjusted seed is not the same seed as the archived off-constraint v18.29 experiment: in that mode, archived profiles are *not compared numerically* and the separate source comparison remains available. A trusted constraint function can only be declared by the researcher after deriving it from the actual model; there is no bundled toy function masquerading as a Q550 invariant.

## Authentic genealogy

`inputs/v18_29_original_server_sendback.zip` is the **unaltered** authenticated genuine Q550 v18.29 server archive. Its SHA256 is pinned in `ENVIRONMENT.json`, and each of its 55 immutable members is checked before anything else. The nested v18.28–v18.11 originals and original scripts are verified by the inherited checkpoint chain. The archive provides the original paired compensated experiment, matched seeds, matrices, time grid, and source state. Python scripts, tests, all necessary readable reference code, run wrappers, requirement list, environment, and hash manifest are included separately in this v18.30 package.

The actual Q550 ODE is loaded from the **unchanged SHA-pinned** server directory:

```
/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle
```

The pinned paths and hashes are encoded in `reference/q550_state_impulse_response_v13.py`. Q550 server code is **not** re-created or substituted with a synthetic approximation; all synthetic ODEs are restricted to unit tests.

## Run on the server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_independent_hessian_constraint_v18_30_bundle.zip
cd q550_kick203_independent_hessian_constraint_v18_30_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_30_server.log
```

For a non-standard source location:

```bash
bash scripts/run_on_server.sh --base-root /absolute/path/to/pinned/original
```

For an **explicitly verified** material invariant module, if you have one:

```bash
bash scripts/run_on_server.sh --constraints-module /absolute/path/to/verified_q550_invariants.py
```

This option must not be used with guessed, artificial or synthetic invariants.

If you only want to verify lineage, synthetic math and input availability **without running any original Q550 integration**:

```bash
bash scripts/run_preflight.sh
```

## Results and sendback

After the full original ODE run, the scripts produce:

- `results/original_independent_hessian_summary_v18_30.csv`
- `results/original_independent_hessian_source_v18_30.csv`: source discrepancy along the trajectory at both steps.
- `results/original_independent_hessian_profiles_v18_30.csv`: RHS-derived profiles vs authentic prior compensated and Jacobian-derived profiles (where seeds are unchanged).
- `results/original_independent_hessian_proof_v18_30.json`: exact source and prior hashes, physical-constraint status, step values and integration counts.
- `results/original_rhs_vs_jac_hessian_v18_30.png`
- `results/original_constraint_hessian_even_profiles_v18_30.png`
- **Only if a constraint plugin was supplied:** `original_declared_constraint_residuals_v18_30.csv` and individual constraint diagnostics.
- `SHA256SUMS_OUTPUT.json`: hashed outputs, inputs, scripts, requirements and README, excluding active `.log` files, runtime-extracted copies and Python bytecode.

The `scripts/pack_sendback.py` gate **refuses** to create a sendback without actual original-Q550 results. With a completed run the resulting archive is:

```
/root/elab1/hysteresis/q550_kick203_independent_hessian_constraint_v18_30_sendback.zip
```

The scripts perform a clean path/hash and packaging audit. All source comments, reporting files and README content are in English.

## Interpretation boundaries

**Evidence of convergence** requires agreement of RHS-derived and Jacobian-derived sources over the original trajectory and agreement of RHS-variational predictions with the independent compensated-pair profiles; agreement of scalar magnitudes alone is weaker than equality of vector profiles. The current historical CSV records **time-local norms**, not the full signed vector from the v18.29 run, so cross-run comparison is explicitly marked **norm-only**. In contrast, the present experiment compares the two source constructions *as vectors* at every timestamp.

None of these tests, with or without a supplied invariant, establishes an intrinsic physical flip, an independently defined material metric, an autonomous constitutive memory, or a global second-order constraint certificate. They resolve a precise local numerical question for the Q550 diagnostic trajectories.
