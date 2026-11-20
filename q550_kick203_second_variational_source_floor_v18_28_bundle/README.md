# Q550 v18.28 — Second-Variational Source & Numerical-Floor Discrimination Audit

## Scope and provenance

This bundle is an **off-constraint original-Q550 11D diagnostic**. The authentic v18.27 server sendback is embedded at `inputs/v18_27_original_server_sendback.zip` and its full nested genealogy is authenticated, member by member. The original nonlinear ODE is NOT simulated or replaced in the offline frozen preflight. The server must have the original SHA256-pinned Q550 support source under `/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle` (the same original source as in v18.27).

The original ODE is only loaded by `scripts/original_second_variational_v18_28.py` on the user's server after all SHA checks pass. Python source and comments are in English. No material invariant/privileged material metric has been supplied; perturbations are expressly **OFF_CONSTRAINT_DIAGNOSTIC**. Do not interpret this as a rigorous second-variation existence certificate or a constitutive memory law.

## Mathematical experiment

Let `y' = F(y)` be the original 11D Q550 ODE with dimensionless time `xi`. Perturb material coordinates only, while retaining a common clock phase. For a direction `v` defined at each anchor:

```
y' = F(y)
u' = DF(y) u,              u(anchor) = (v,0)
w' = DF(y) w + D²F(y)[u,u],  w(anchor) = 0
```

The full base state `y` has 11 entries; `u` and `w` have ten material entries each (their phase perturbations are zero). The same base state is propagated both backward and forward from the anchor. The variational forcing is evaluated directly from the original RHS, **independently of the nonlinear paired trajectories**:

- `DF(y) u`: fourth-order centered directional first differences at a fixed absolute state displacement 0.004.
- `D²F(y)[u,u]`: fourth-order centered *five-point* directional Hessian difference. Compare three absolute directional displacements 0.005, 0.02, and 0.08, spanning a factor of sixteen; predictions use the middle value and the outer values diagnose finite-difference sensitivity.
- Directional displacements are applied to unit-normalized material directions and rescaled by the tangent norm; they are **not** proportional to the small physical pair amplitude `epsilon`.

For true separately integrated trajectories `y_plus`, `y_minus`, `y0`:

```
R_plus  = H (y_plus  - y0) / epsilon
R_minus = H (y_minus - y0) / epsilon
R_even  = (R_plus + R_minus)/2 = epsilon/2 H w + O(epsilon^3)
R_odd   = (R_plus - R_minus)/2 = H u + O(epsilon^2)
```

The three displayed terms on the right are *local expansions*, not exact finite-amplitude identities. The ratio of the independently predicted even response to the difference between the outer Hessian finite-difference stencils is a **sensitivity diagnostic only**, not a rigorous error bound. Convergence of the source with stencil size and the agreement with original nonlinear paired trajectories must both be checked.

### Selected probes

- `material3`, anchor `xi=3.5`
- `material3`, anchor `xi=4.5`
- `raw4`, anchor `xi=4.0`
- `raw6`, anchor `xi=4.5`

The observer matrices are the same constant projections as in v18.20–v18.27, using archived authentic 10D mode directions. All four tangent seeds originate in the authenticated v18.20 hidden-direction audit, transported by the authenticated archive cocycle. New nonlinear paired amplitudes: `1e-5` and `1e-6`. Exact common sampling grid: 17 historical samples (`xi_anchor - 0.5` to `xi_anchor`) plus three future samples (`+0.2`, `+0.5`, `+1.0`). The exact same grid is used for full second-variational and paired nonlinear solves. Independent baseline, plus and minus physical ODE trajectories are re-integrated.

## Run on the server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_second_variational_source_floor_v18_28_bundle.zip
cd q550_kick203_second_variational_source_floor_v18_28_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_28_server.log
```

Use `bash scripts/run_preflight.sh` for an **offline authentication and synthetic math test only**. It cannot certify the original Q550 second variation.

The server run writes:

- `results/original_second_variational_proof_v18_28.json` — the original ODE execution/provenance gate;
- `results/original_second_variational_pairs_v18_28.csv` — independent even/odd vs second/first variational comparison;
- `results/original_second_variational_profiles_v18_28.csv` — signed-pair magnitudes at each actual xi sample;
- `results/original_second_variational_sources_v18_28.csv` — the independent second-variational forcing along the orbit;
- `results/original_second_variational_vs_pairs_v18_28.png` and `results/original_second_variational_profile_v18_28.png` — visual audits.

After tests, original-source verification, all three Hessian stencils, independent paired nonlinear integrations and manifest checks pass, the script creates:

```
/root/elab1/hysteresis/q550_kick203_second_variational_source_floor_v18_28_sendback.zip
```

The sendback packager **refuses** to package an offline preflight as a completed original ODE result. It excludes active `.log` files, Python caches and `.runtime` scratch input extractions to avoid self-modifying hash manifests. The entire source genealogy is included as the exact nested server sendback, not just its plots or CSV files.

## Interpretation rules

1. If the fourth-order Hessian source is stable across absolute steps 0.005, 0.02, and 0.08, and its propagated second variation agrees with independently integrated plus/minus even responses at sufficiently resolved epsilon, this supports a finite **quadratic nonlinear source** in the original support ODE for these probes.
2. If the source changes strongly with stencil size, or the original even pair comparison is buried below numerical cancellation, label the result **INCONCLUSIVE**, not `zero` or `hysteresis proven`.
3. Zero clock phase difference and a common original 11D state at the start are required, but opposite perturbed *material* states are distinct. These experiments cannot prove an autonomous constitutive memory or an invariant constrained material torque.
4. The previous v18.27 two-DOP853-tier difference is an empirical floor indicator, not a certified numerical error bound.

## Environment

Python >=3.10, numpy, scipy, matplotlib. All scripts and input hashes are included. `ENVIRONMENT.json` identifies **v18.28** and its actual **v18.27** parent (the old v18.27 bundle had an incorrectly inherited v18.26 label).

**Scale warning:** Some genuine material state coordinates are much smaller than the finite-difference displacement. The emitted `max_relative_state_displacement_*` diagnostics identify when the directional stencil is not small relative to individual state coordinates. Agreement of finite stencils alone is not proof of a local derivative; any nonlocality must remain explicitly documented.
