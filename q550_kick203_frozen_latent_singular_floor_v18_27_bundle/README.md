# Q550 v18.27 — Frozen-Latent Basis, Singular Subspace & Numerical-Floor Audit

**Status at distribution:** Original nonlinear **v18.26** reduced data have been
SHA256-authenticated and independently reanalyzed. The new **v18.27** stringent
DOP853 accuracy comparison has **not yet been run on the original Q550 server**.
Do not confuse the completed cached-data analysis with the pending high-precision
nonlinear floor test. The bundle packager refuses to create a certified sendback
without that test.

## Research question

The v18.26 server run reported a useful rank-20 predictor at epsilon=1e-5;
refitting at shrinking amplitudes lost most of that advantage, whereas reusing
the original frozen rank-20 predictor largely preserved it. The new audit asks:

1. Is the **ten-dimensional leading history subspace** stable across amplitudes?
2. Does the **rank-20 subspace** follow a stable weak singular tail or rotate
   strongly as finite precision and/or nonlinear weak components change?
3. Is an apparent change of latent *basis* merely a **coordinate gauge**
   change that leaves predictions invariant?
4. Can the high-accuracy original nonlinear ODE resolve the plus/minus even
   response above integration/cancellation error at very small epsilon?

## Scientific separation / NO PHYSICAL CLAIM

SVD vectors live in the standardized reduced-history feature space, not in
an intrinsic material frame. Near-degenerate tiny singular directions are
especially free to rotate. Rank 20 is a **predictive embedding dimension**, not
20 physical degrees of freedom. All perturbations remain local off-constraint
diagnostics. This audit does **not** demonstrate a constitutive material
memory, a privileged metric, or a physical torsional flip.

The source data derive from original-Q550 nonlinear integrations verified in
the v18.26 sendback. The sensor-only analysis script neither imports nor calls
the ODE. It uses *train* past histories for the SVD, validation futures for
model selection, and untouched test futures only for scoring. Within each
noise protocol it uses the same synthetic noise draw at each epsilon, with
the correctly changed normalized noise scale for fixed absolute noise.

## Scope and provenance

`inputs/v18_26_original_server_sendback.zip` is the **authentic server archive**
from v18.26, including its executable v18.25 ancestor and all earlier nested
provenance. Every SHA256 listed by that server is verified before analysis;
the original nonlinear ODE completion proof is independently read. There is
one ZIP root directory only: `q550_kick203_frozen_latent_singular_floor_v18_27_bundle`.

The original RHS on the user's server remains pinned by three SHA256 hashes
provided through `reference/q550_state_impulse_response_v13.py`. Those exact
external original Q550 source files must remain installed under the existing
`/root/elab1/hysteresis/q550_full11D_transverse_slow_state_dense_sampling_v1_bundle`.
No rewrite or replacement of that reference RHS is performed.

### Cached nonlinear analysis (already completed)

- 3 observer families; 5 amplitudes (1e-5 to 1e-7); 3 noise protocols.
- 45 singular spectra and 90 reference-relative subspace comparisons.
- 270 refitted-vs-frozen held-out prediction scores, **independently reproduced**
  against original v18.26 CSVs.
- SHA-checked reconstruction of 45 old even/odd probe diagnostics.
- SVD bases, singular values, normalization and predictive coefficients saved
  to `results/original_latent_bases_v18_27.npz` with their generating source.
- Left/right latent gauge invariance tested: `V -> V Q`, `beta -> Q^T beta`.

Key reference result for **material3 with zero added noise**, relative to the
reference basis at amplitude 1e-5:

| amplitude | largest principal angle, rank 10 | rank 20 |
|---|---:|---:|
| 1e-5 | 0 deg | 0 deg |
| 3e-6 | 0.00313 deg | 79.71 deg |
| 1e-6 | 0.00803 deg | 83.14 deg |
| 3e-7 | 0.03439 deg | 87.02 deg |
| 1e-7 | 0.05956 deg | 89.49 deg |

The tail energy from singular directions 11 through 20 is only ~9.76e-15 of
total standardized-sample energy at 1e-5, growing to ~1.20e-11 at 1e-7.
This very weak tail is a **warning**: it can react strongly to numerical noise.
At the smallest epsilon, the standardized feature scale drift from the
reference `material3` frame is ~2.15e-6, much smaller than the tail subspace
rotation (but not a gauge-invariant measure of physical motion).

Previous parent results for material3 at xi=3.5, no added noise, are exactly
reproduced: rank10/rank20 score ratio 3.453 at 1e-5, 1.006 when refitted at
1e-7, but 2.833 when the original 1e-5 rank-20 predictor is frozen.

### Pending narrow original-ODE check

The server command reruns **272 short integrations** in total, not 400 orbits
and not the v18.26 full 1,596-integrations batch. For 3 observer families x
3 sections x 5 amplitudes, it computes nonlinear +epsilon / -epsilon and
center baselines under two solver settings, sharing the same pinned RHS:

- reference: DOP853 rtol=5e-11, atol=6e-12, max step=0.04 xi
- tight: DOP853 rtol=3e-13, atol=3e-14, max step=0.01 xi

The **inter-tier disagreement** of the normalized *even* response is a
practical integration-sensitivity indicator, **not** a rigorous error bound.
The test must not claim a quadratic material law when a supposed even signal
is similar to, or smaller than, inter-tier disagreement. We retain a separate
empirical proxy `epsilon * even_rms` from the v18.26 observations.

## Exact server commands

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_frozen_latent_singular_floor_v18_27_bundle.zip
cd q550_kick203_frozen_latent_singular_floor_v18_27_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_27_server.log
```

The command first runs unit tests and authenticates the v18.26 parent; then
repeats only the targeted original-Q550 floor comparisons, regenerates the
plots, updates the manifest, and packs the sendback. The original `tee` log is
**never hashed or packed**. The `.runtime` nested-archive extraction is also
excluded from output hashes.

Expected sendback at:

`/root/elab1/hysteresis/q550_kick203_frozen_latent_singular_floor_v18_27_sendback.zip`

Offline-only recheck without original RHS:

```bash
bash scripts/run_preflight.sh
```

## Output files

- `results/original_singular_spectrum_v18_27.csv`
- `results/original_principal_subspace_v18_27.csv`
- `results/original_model_reproduction_v18_27.csv`
- `results/original_gauge_invariance_v18_27.csv`
- `results/original_latent_bases_v18_27.npz`
- `results/original_parent_even_odd_floor_proxy_v18_27.csv`
- `results/original_subspace_stability_v18_27.png`
- `results/original_singular_gap_v18_27.png`
- `results/original_subspace_summary_v18_27.json`
- **server only:** `results/original_tight_floor_comparison_v18_27.csv`
- **server only:** `results/original_high_precision_floor_proof_v18_27.json`
- **server only:** `results/original_tight_floor_v18_27.png`

## Reproduction and limitations

Versions and library requirements are in `ENVIRONMENT.json` and
`requirements.txt`; test and generating Python sources are within `scripts/`
and `tests/`. `scripts/build_manifest.py` builds `SHA256SUMS_OUTPUT.json`.
`pack_sendback.py` refuses any run lacking proof of all 45 original nonlinear
accuracy rows (272 newly executed short integrations).

Any reported principal angles are relative to the standardized reduced
history representation and depend on observation metric/scaling. The
inter-tier solver comparison cannot *prove* numerical convergence, and
machine precision may limit epsilon=1e-7 even when solver tolerances shrink.
