# Q550 v18.26 — Vanishing-Amplitude Latent Rank & Transport Robustness Audit

## Scientific question

At v18.25, a predictive latent rank of 20 outperformed rank 10 at shifted
postures in some low-noise tests, while a paired-history affine transport made
their performances nearly indistinguishable. Is the apparent rank-20 advantage
an amplitude-dependent nonlinear effect, or does it survive in the linear limit
through observer gauge, finite sample estimation or regularization?

**No extra physical 10D directions or constitutive memory are assumed.** All
Q550 perturbations in this experiment are off-constraint diagnostics.

## Experiment design

- **Five amplitudes:** `1e-5`, `3e-6`, `1e-6`, `3e-7`, `1e-7` (default).
- **Three section anchors:** `xi = 3.5, 4.0, 4.5`. These change both material
  posture and clock phase, not merely the phase.
- **Identical seeded direction cohorts at all amplitudes:** 96 reference
  training, 32 validation and 36 random out-of-training test directions.
  One additional old certified matched hidden-direction probe per observer
  makes **37** test trajectories. At each shifted section, the first 32
  training directions provide paired *past-only* calibration histories.
- **Three reduced observers:** `material3`, `raw4`, `raw6` (the material3
  projection itself originates from older ODE-aware diagnostics).
- **Two candidate ranks:** 10 and 20, *never* forced to a known physical
  dimension. Reference rank selection uses **reference validation futures
  only**, never shifted/test futures.
- **Four model comparisons:** unaligned (`none`), orthogonal latent transport,
  affine-ridge latent transport and deliberately wrong-pair orthogonal
  transport as a negative control. Transport fitting sees **paired past
  observations only**, never future labels.
- **Three observation-noise protocols** on the *amplitude-normalized* reduced
  response `(z_eps-z_0)/eps`:
  1. no synthetic noise;
  2. fixed normalized noise `sigma=1e-4`;
  3. fixed absolute reduced-observation noise `sigma_raw=1e-9`, which becomes
     `sigma_normalized=1e-9/eps`, increasing from `1e-4` to `1e-2` as the
     perturbation amplitude decreases by 100×.
  Synthetic noise never contaminates clean future labels; all estimates
  are evaluation conventions, not measured sensor uncertainties.
- **Matched-amplitude fit**, plus a separate **frozen-reference model** fitted
  only at `eps=1e-5` and tested at all smaller amplitudes, without refitting.
  This separates model adaptation from transport across amplitudes.
- **Independent +epsilon/-epsilon hidden probes:** measure the even component
  `(R(+eps)+R(-eps))/2` and the odd component
  `(R(+eps)-R(-eps))/2` of the *normalized* response. Compare odd response to
  the previously certified tangent propagator, assessing the numerical
  differencing/interpolation floor before interpreting an apparent scaling law.

All trajectories come from an independently loaded, SHA256-pinned **original
Q550 11D ODE on the server**. The ODE oracle is separate from the estimator:
`scripts/amplitude_math_v18_26.py` accesses neither equations nor any hidden
state / Jacobian / cocycle. It receives reduced histories and reduced futures.

## Server workflow

From `/root/elab1/hysteresis` (or the matching server working directory):

```bash
unzip q550_kick203_vanishing_amplitude_latent_transport_v18_26_bundle.zip
cd q550_kick203_vanishing_amplitude_latent_transport_v18_26_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_26_server.log
```

The runner prefers `python3.13` and falls back to `python3`; dependencies are
listed in `requirements.txt`. It uses the existing original Q550 server bundle
at `/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle`
(override with `--base-root PATH` if necessary), and validates all original
source hashes. **It does not regenerate the 400-period orbital run.** It does
perform approximately **1,600 new independent local nonlinear integrations**
(including paired negative probes and baselines), so it is materially heavier
than v18.25. A run cannot be certified without them.

Generated artifact in the parent working directory:

`q550_kick203_vanishing_amplitude_latent_transport_v18_26_sendback.zip`

Send this archive back for analysis.

### Frozen preflight ONLY

```bash
bash scripts/run_preflight.sh 2>&1 | tee v18_26_preflight.log
```

The frozen preflight uses the authenticated original archived *linear* tangent
propagator. It checks (a) no amplitude-dependence arises in a strictly linear
trajectory under identical normalized noise, (b) the fixed-absolute noise
protocol increases its normalized noise floor as epsilon shrinks, and (c)
all model / calibration code runs without inspecting test futures. **It is
not original nonlinear evidence.** The sendback packager refuses to operate
on preflight-only results.

## Outputs

Server-only files under `results/`:

- `original_amplitude_prediction.csv`: full paired predictor metrics.
- `original_rank20_vs_10.csv`: per-case *out-of-sample* rank-10/rank-20 error
  ratio. **Ratio > 1** favors rank 20; ratio < 1 favors rank 10.
- `original_rank_selection.csv`: validation scores and chosen ranks.
- `original_calibration.csv`: history-only transport calibration.
- `original_frozen_reference_transfer.csv`: frozen model trained at large
  amplitude, scored on all smaller amplitudes.
- `original_even_odd_probe.csv`: independent ±epsilon probe decomposition,
  including numerical tangent comparison.
- `original_reduced_dataset_v18_26.npz`: reduced observed histories and
  reduced future labels for fully reproducible model-only reanalysis; no full
  11D state is supplied to the predictor.
- `original_summary.json`, `original_ode_amplitude_proof.json`: provenance
  and original nonlinear execution status.
- `original_rank_survival_vs_amplitude.png`,
  `original_noise_floor_vs_amplitude.png`, `original_even_odd_scaling.png`:
  non-linear server-only plots.

Frozen-only outputs have `frozen_` prefixes and must not be reported as
nonlinear amplitude scaling. The `SHA256SUMS_OUTPUT.json` file covers all
immutable scripts, inputs and outputs. `.runtime/`, `.log` and `__pycache__`
files are excluded to avoid hashing active logs.

## Verification and interpretive limits

1. Equal phase of perturbed and reference trajectories is checked directly;
   an integration fails if the phase mismatch exceeds `1e-8`.
2. Small-amplitude drift of the normalized response may be numerical
   cancellation, solver tolerance or tangent interpolation error. Plot and
   report the even-odd probe floor, not only latent-rank ratios.
3. The five points constitute a **finite amplitude scan**, not a mathematical
   proof of a limit as `eps -> 0`. The off-constraint trajectories do not
   certify constitutive hysteresis or a physically preferred material metric.
4. Unknown pair correspondence would prevent this exact calibrated transport
   workflow. Pair labels are additional information available only during
   past-history calibration.
5. Original source dependencies must exactly match the pinned hashes from
   `reference/q550_state_impulse_response_v13.py`.
6. Normalized `eps` perturbations are local around the same fixed Q550
   reference baseline at each section; no generalization to unrelated
   orbits is claimed.

## Reproducible lineage

`inputs/v18_25_original_server_sendback.zip` is the authentic completed v18.25
server sendback, embedding its full previous archive ancestry. The new
`checkpoint_io_v18_26.py` authenticates all archived immutable files and
nonlinear completion status, then delegates to the earlier versioned
checkpoint readers in `scripts/`. The new estimator, oracle, tests, plotter,
manifest builder, requirements and executable runners are all included.
See `ENVIRONMENT.json` for the pinned parent SHA256. No historical source
scripts or results are silently replaced.
