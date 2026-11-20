# Q550 v18.34 — Transport-Defect Budget & Overlap-Gauge Coherence Audit

## Purpose

The authentic v18.33 server run found close alignment of locally fitted
surface normals but large finite-time violations of the fitted cofactor law.
This audit **does not search for new invariants**. It decomposes the observed
finite-time defect by integrating the local Lie-cofactor residual along the
**original independently propagated Q550 trajectories**. It also measures
*when trajectories depart* from the diagnostic normalized coordinate region
where the surfaces were fitted, and audits normal-angle sensitivity to the
choice of diagnostic metric. A close surface-normal match is not evidence of
material invariance.

## Derivation

For each fixed original v18.33 candidate `C(y)=phi(y) @ q` and cofactor
`mu(y)`, let `r(y)=D C(y) F(y) - mu(y) C(y)` and
`M(t)=int_0^t mu(y(s)) ds`. Exactly,

    C(y(T)) - exp(M(T))*C(y(0))
      = exp(M(T)) * int_0^T exp(-M(s))*r(y(s)) ds.

We sample `C`, `D C F`, and `mu` on independent original Q550 DOP853
trajectories and integrate the residual numerically with cumulative Simpson
and trapezoidal quadrature. Reported quadrature closure is an **algebraic
consistency test**, not a proof of physical invariance or a rigorous error
bound. Signed time-bin contributions account for cancellations. The same
surface coefficients are used throughout; the finite differences between
windows are diagnosed but never interpreted as a physical gauge.

## Controlled experiment

- Fixed two candidates selected **before** this new run from v18.33's
  training-only shortlist: phase-covariant and phase-blind quadratic surfaces
  with constant cofactor `mu=-1`.
- Reconstruct the seven original anchor states, center, scale, phase origin,
  training and independent testing probes deterministically.
- Regenerate the 12 exact prior projected seeds (two candidates × three
  posture anchors 3.5/4.0/4.5 × two seeds).
- Run 12 original Q550 short ODE trajectories from the projected seeds;
  plus one anchor-state integration, no 400-orbit replay.
- Check all 36 prior endpoint values at durations 0.25, 0.5, and 1.0 xi.
- Follow `r(xi)`, cumulative signed contributions, unsigned cancellation,
  quadrature closure, and crossings of radii 1, 3, 10 in normalized 10D.
- Refit the local training-only overlapping windows and compare unoriented
  normals under three explicitly declared *diagnostic* diagonal metrics;
  verify the original gauge and orientation-flip invariance.
- No clock-period or material Poincare return is claimed.

## Installation and server run

From `/root/elab1/hysteresis`:

```bash
unzip q550_kick203_transport_defect_overlap_gauge_v18_34_bundle.zip
cd q550_kick203_transport_defect_overlap_gauge_v18_34_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_34_server.log
```

Expected deliverable in `/root/elab1/hysteresis/`:
`q550_kick203_transport_defect_overlap_gauge_v18_34_sendback.zip`.

The original external Q550 ODE modules must already be installed in the
original SHA256-pinned server directory identified in
`reference/q550_state_impulse_response_v13.py`. `requirements.txt` lists
Python dependencies. To authenticate the parent archive and run synthetic
methodology tests without the original external ODE, run
`bash scripts/run_preflight.sh`.

## Outputs

- `original_v18_34_proof.json` — original integration/genealogy provenance and
  numerical-closure diagnostics.
- `original_v18_34_budget_samples.csv` — sample-by-sample `C`, cofactor,
  defect source, transport predictions, integrated budget, diagnostic radius.
- `original_v18_34_budget_endpoints.csv` — endpoint closure, source
  cancellation, first diagnostic-radius crossing and historic replay check.
- `original_v18_34_budget_segments.csv` — signed subinterval contributions
  to each requested endpoint.
- `original_v18_34_overlap_gauge.csv` — normal angles under alternative
  explicitly diagnostic reweightings, with sign-gauge controls.
- `original_v18_34_budget_closure_*.png`, `original_v18_34_source_profile.png`,
  `original_v18_34_domain_exit.png` — derived plots generated only after the
  original Q550 ODE test.

## Scientific limitations

All tested projected perturbations are off-constraint unless an independent
material constraint is discovered. No privileged material metric, manifold,
physical torsion, constitutive memory, interval certificate, or genuine
material return follows from this study. A large extrapolation beyond the
training neighborhood can invalidate local geometric interpretations even
when the cofactor identity holds exactly along the full flow. Residual
integration verifies numerical and algebraic bookkeeping, not physical
validity of the hypothesized surface. Normal-angle comparisons depend on the
coordinate metric; coherent rescaling of `q` by a nonzero scalar changes
neither the zero set nor the unoriented normals.

## Reproducibility

All newly written scripts and tests, English documentation, full original
v18.33 zipped sendback, reference scripts inherited from v18.33, exact
parent archive SHA256, dependency list, and SHA256 file manifest are shipped.
The embedded v18.33 ZIP retains its original complete ancestor genealogy.
Runtime-extracted archives and active tee logs are excluded from manifests.
The packager refuses preflight-only data and verifies the final archive root.
