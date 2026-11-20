# Q550 v18.36 — Flow-Aligned Local Support & Normal-Transport Audit

## Scientific objective

The original v18.35 found only four of twelve historical seeds inside its diagnostic calibration support, and those four exited within ~0.9–3.3e-6 xi. This audit precommits NEW independent initial seeds, projects onto the two **frozen and rejected** v18.33 candidate levels, and admits them only if BOTH scaled material radius and phase fall strictly within the training-only support.

This is not a physical invariant-manifold certificate. An exactly flow-advected surface is invariant by construction, so it is **not evidence** for a physically privileged material surface. Here we test whether the *same candidate equation C* remains tangent/coherent against a transported normal covector when evaluated on new independently evolved states. No material metric is certified; angle metrics are declared diagnostics. Tests with off-constraint probes must not be promoted to physical constraints.

For each seed, integrate y_seed and phase-aligned y_reference with original pinned Q550 ODE, alongside normalized-coordinate tangent u'=B u, transported candidate conormal m'=-B.T m, and integrated source Z'=exp(-mu*t)(L_F C-mu C), with B=S^-1 J_xx S. Compare m(t) with grad_x C(y_seed(t))*S. Monitor C, source, source integral, co-moving distance, support exits, signed and gauge-stretched normal angles, and cotangent-tangent pairing. Pairing preservation is a mathematical identity/control, not independent physics.

Six configurations (two frozen surfaces × three anchor postures), two precommitted independent seeds each (12 total), one baseline original ODE replay, 13 original local integrations. Time interval T=1e-5 xi, 146 or more distinct time samples. No 400-orbit replay.

## Run

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_flow_aligned_support_normal_transport_v18_36_bundle.zip
cd q550_kick203_flow_aligned_support_normal_transport_v18_36_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_36_server.log
```

Output sibling: `q550_kick203_flow_aligned_support_normal_transport_v18_36_sendback.zip`.

`bash scripts/run_preflight.sh` authenticates v18.35 only; it never certifies a new Q550 result. Parent ZIP is pinned byte-for-byte including the complete executable genealogy. The original Q550 source is loaded from the SHA-pinned unchanged server dependencies, not supplied as a copy.

## Interpretation safeguards

- `C=0` is a fitted diagnostic zero level, **not** a proven constraint.
- Support radius 0.8 and phase half-band 0.25 rad are training-only diagnostics; belonging to that ball is not a strict statistical support certificate.
- The cotangent transported by -B.T is the mathematically advected conormal and must not be interpreted as a discovered invariant by itself.
- Only **within-support** discrepancies and out-of-sample tests can assess the frozen C candidate locally. Report `OUTSIDE_AT_START` separately from true crossings.
- A small angle depends on declared coordinate gauge, and normal agreement alone is insufficient without Lie/cofactor tangency and geometric support.
- No true clock return or material return is measured in this micro-time window.

## Inputs and provenance

`inputs/v18_35_original_server_sendback.zip` authentic original Q550 v18.35 including v18.34 and full nested history; SHA recorded in `ENVIRONMENT.json`. `scripts/checkpoint_io_v18_36.py` validates the parent and stages the immutable v18.34 input for historical certified load routines. Every Python script actually used is included, plus all historical scripts, requirements, tests, results, manifest, and Q550 original source SHA pins.
