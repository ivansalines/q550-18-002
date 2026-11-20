# Q550 v18.29 — Second-Variational Convergence & Compensated-Pair Floor Audit

## What this does

A targeted, **off-constraint** original-Q550 11D diagnostic. The main probe is `raw6` at anchor `xi=4.5`, where v18.28 reported a second-variation prediction of `4.648849977913204e-7` versus an independently measured normalized even response of `4.7068733317233505e-7` at `epsilon=1e-5`. The second probe (`material3`, anchor `3.5`) is an intentionally weaker control, not a claim of a privileged material metric.

The **original v18.28 server sendback**, `inputs/v18_28_original_server_sendback.zip`, is carried **unaltered**, SHA256 pinned in `ENVIRONMENT.json`, with nested v18.27–v18.11 provenance and runnable Python reference source. Every member in its SHA256 manifest is verified before any original-Q550 numerical integration. No past script is replaced with invented code. The original Q550 RHS and original Jacobian are dynamically loaded from the same server path pinned in `reference/q550_state_impulse_response_v13.py` after exact SHA256 checks.

Original ODE source location (server only): `/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle`. The Jacobian callable originates in its SHA256-pinned `test_support_q550_exact_nonlinear_local_tube_v2_1.py`. An independent directional RHS finite-difference sanity check is performed before the Jacobian-integral solves; its empirical error and the full results are reported. The Jacobian's internal derivation is not independently certified by this audit. There is **no original Q550 ODE run in the offline preflight**.

## Why a compensated pair?

The conventional normalized even signal uses three separately integrated 11D states, potentially containing material coordinates of order thousands:

```
R_even = H (y_plus + y_minus - 2*y_base) / (2*epsilon)
```

If `epsilon` is small, subtraction of large nearly equal numbers can dominate the true O(epsilon) normalized even signal.

Instead define two **small difference states** `delta_plus = y_plus - y_base` and `delta_minus = y_minus - y_base` and propagate their dynamics directly. For a differentiable autonomous field `F`,

```
delta' = F(y + delta) - F(y)
       = (integral_0^1 J(y + t*delta) dt) delta,
J = DF,  y' = F(y).
```

The code evaluates the segment integral by **three-point Gauss-Legendre quadrature** using the original pinned Q550 Jacobian. It solves one augmented 31D system containing the base 11D trajectory, `delta_plus` (10 material coordinates), and `delta_minus` (10 material coordinates). The phase difference is identically zero. No large-state subtraction is required to evolve the small differences. The final even observable still adds the two small `delta` states and can incur small-amplitude cancellation; this approach *reduces* the floor rather than rigorously eliminating it.

The independently predicted second variation follows

```
u' = J(y) u
w' = J(y) w + D(J)(y)[u] u
R_even_predicted = (epsilon / 2) H w.
```

This run evaluates `D(J)[u]u` by a **four-point, fourth-order centered derivative of the pinned original Jacobian**, at absolute material directional displacements `h=0.01` and `h=0.04`. That is methodologically different from v18.28's five-point second directional **RHS** differences (`h=0.005,0.02,0.08`). Thus there are three quantitative witnesses:

1. Original v18.28 *independently integrated conventional* +/- pair and RHS-derived second variation (archived, authenticated).
2. v18.29 integrated small-difference compensated pair via a Jacobian **line integral**, with two ODE tolerance tiers.
3. v18.29 independently propagated Jacobian-derived second variation, with two Jacobian derivative stencils.

They share the **same original Q550 ODE**; the calculations are independent numerical methods, not statistically independent physical experiments. In particular, the Jacobian-integral method requires an adequately accurate original Jacobian, which is independently spot-checked but not interval-certified.

## Grid, probes and convergence gates

- `raw6`, anchor `xi=4.5`: primary signal.
- `material3`, anchor `xi=3.5`: negative/sensitivity control.
- Perturbation amplitudes `epsilon = 1e-5, 3e-6, 1e-6`.
- Historical samples: 17 timestamps over the preceding 0.5 xi; future samples: `+0.2, +0.5, +1.0 xi` (20 unique timestamps including anchor).
- Original Q550 baseline is integrated independently from the authenticated `xi=0` state to each anchor, with original pinned `support_rhs_float`.
- `standard`: DOP853, `rtol=5e-11`, `atol=5e-12`, max step `0.035 xi`.
- `tight`: DOP853, `rtol=3e-13`, `atol=3e-14`, max step `0.0125 xi`.
- Estimated numerical precision is **empirical**: compare normalized even signals between solver tiers, between source stencils, and to the independently archived v18.28 conventional pair.
- All perturbations are off-constraint diagnostic and **do not imply** a material memory law, physical angular flip, unique intrinsic metric, or interval-certified Hessian.
- `xi` is the dimensionless archive coordinate; the pinned original RHS is scaled by the archived `slope` as in v18.28.

## Run on the server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_second_variational_compensated_v18_29_bundle.zip
cd q550_kick203_second_variational_compensated_v18_29_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_29_server.log
```

If the original pinned source lives at a nonstandard location, append `--base-root /absolute/path` to the Python driver argument via `bash scripts/run_on_server.sh --base-root /absolute/path`.

The run performs **approximately 34** local ODE integrations in total: 2 anchor baselines, 8 two-sided independent source-varied integrations, and 24 two-sided compensated-pair integrations. Runtime depends strongly on the original pinned Jacobian evaluation; this is not a cheap scalar regression and may be slower than expected from the count. No 400-period orbit is regenerated.

Expected return artifact:

```
/root/elab1/hysteresis/q550_kick203_second_variational_compensated_v18_29_sendback.zip
```

Contains the complete executable lineage and outputs:

- `results/original_compensated_proof_v18_29.json` — original-Q550 execution gate and source provenance.
- `results/original_compensated_pairs_v18_29.csv` — six comparisons, with old conventional floor, new compensated response, independent second-variation predictor, two solver-tier differences and Hessian-step spread.
- `results/original_compensated_profiles_v18_29.csv` — time-resolved even/odd responses for standard and tight tiers.
- `results/original_jacobian_source_v18_29.csv` — independently evaluated Jacobian Hessian-source diagnostics along the original state.
- `results/original_compensated_floor_comparison_v18_29.png`, `results/original_compensated_profile_v18_29.png` — original ODE plots.
- `results/frozen_preflight_v18_29.json` — source authentication and historical result only.
- `SHA256SUMS_OUTPUT.json` — hashes all immutable files, excluding `.runtime`, Python caches and active `.log` files.

**Packager refuses** to emit the purported original-Q550 server sendback without actual six-case nonlinear proof. With preflight only, use `bash scripts/run_preflight.sh`; it cannot make the server artifact.

## Interpretive decision rule

- If compensated even responses track the independent second variation down to `epsilon=1e-6` with solver-tier and Jacobian-stencil discrepancies smaller than the signal, while the archived separately integrated conventional pairs depart from it, the previous discrepancy is consistent with **large-state cancellation error**.
- If the Jacobian-integral and Jacobian-differentiated second-variation methods disagree or the solver tiers fail to converge, report **INCONCLUSIVE**, especially when source steps are nonlocal relative to small material coordinates.
- Neither agreement nor disagreement certifies an invariant-constrained second-order geometric torsion or an autonomous constitutive memory.

All source code, README text, and script comments use English. The experiment is numerically falsifiable; it makes **no claims about results that have not yet run on the original Q550 server**.
