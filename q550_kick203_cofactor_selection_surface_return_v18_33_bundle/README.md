# Q550 v18.33 — Cofactor Selection Repair & Surface-Return Coherence Audit

## Scientific objective and scope

The v18.32 original-server experiment fitted 40 material and phase-covariant level-set equations `C(x, theta) = 0` with trial Lie cofactors `mu(theta) = lambda + mod*sin(theta-theta0)` and tested the candidate relation `L_F C = mu C`. Four finalists were selected by the smallest ratio of singular values, not by the normalized residual of the fitted Lie-cofactor equation. That selected three models with training relative defect exactly **1** while overlooking an explicitly phase-covariant quadratic model with training relative defect approximately `3.3223310786e-4`.

v18.33 repairs **only the selection criterion**, preserving the exact v18.32 training and holdout seeds/dictionaries, and then tests whether the *same fitted level-set relation* persists across overlapping posture windows and local phase-clock returns. A clock-phase return is not a Poincare return of the material state; this audit does not certify global recurrence, a physical constraint, constitutive memory, or an intrinsic torsional flip.

## Original and reproducible provenance

- The single full, original server sendback from v18.32 is **embedded unchanged** in `inputs/v18_32_original_server_sendback.zip`. It includes v18.31, v18.30, and the recursively nested scripts and data in the certified genealogy.
- `scripts/checkpoint_io_v18_33.py` verifies the v18.32 archive SHA256, ZIP root, per-file manifest, original Q550 proof, and the SHA of its nested v18.31 ancestor. It then delegates to the SHA-pinned ancestor loader used by previous audits. The original model is loaded from the unchanged SHA-pinned source files on the server, not from a surrogate or reconstructed ODE.
- `ENVIRONMENT.json` documents hashes and all parent paths. `scripts/build_manifest.py` excludes active `*.log`, temporary `.runtime`, `.pyc` and caches. `scripts/pack_sendback.py` is fail-closed until the new original experiment outputs exist and are SHA verified.
- The unmodified v18.32 server experiment and associated scripts are contained in the nested original ZIP. All new v18.33 scripts, synthetic tests and outputs are kept at the current ZIP root. Source comments and documentation are in English.

## Experimental protocol (selection and tests separated)

1. Authenticate the original v18.32 sendback and reconstruct seven original Q550 anchor states at `xi=[3.25,3.5,3.75,4,4.25,4.5,4.75]`. Sample exactly **392 training states** and **224 independent holdout states**, using the identical original field, seeds and normalized material coordinate system as v18.32.
2. Refit the **same 40** polynomial/phase-covariant models. Confirm each training residual reproduces the v18.32 recorded training score within `3e-7`. **Rank solely by the training normalized Lie-cofactor residual** (`ensemble_score.relative_residual`), not the singular min/max ratio. Break ties by model dimension and deterministic name. Do not inspect any holdout score when choosing final candidates.
3. Select the **best 3 phase-blind and best 3 phase-covariant** training models, plus two preregistered historical v18.32 control choices (deduplicate if needed). The overlooked phase-covariant quadratic `lambda=-1, mod=0` is required to appear in the shortlist by the ranking itself, not by forcing the outcome.
4. Score each finalist on held-out transverse states, seven individual postures and phase shifts `theta ±0.6`. Project independent seed states onto the global candidate level set using the **diagnostic normalized-coordinate Euclidean metric**, measure projected Lie tangency, and integrate independent Q550 trajectories for elapsed `xi=0.25, 0.50, 1.00`. Compare `C(t)` against its predicted cofactor transport `C(0)*exp(integral mu dt)`. These are **not** new physical invariants.
5. For three overlapping training windows (`anchors 0:4`, `2:6`, `3:7`) independently refit each finalist using **only training states**. Evaluate each refit and the global candidate at **the same overlapping anchor states**, gauge-aligning normals up to sign. Record normalized-coordinate normal-angle mismatch and local level offset. This explicitly tests whether one fitted geometric equation carries coherently across posture windows. It does not establish a canonical material normal.
6. At `delta_xi=1.0`, record the observed phase-clock increment, wrapped angular error, and separately the *material displacement*. The label **CLOCK_PHASE_RETURN_ONLY_NOT_MATERIAL_POINCARE_RETURN** is essential: a `2*pi` clock return cannot be interpreted as a returning material orbit without an independent return condition.
7. Report the complete candidate ranking, zero-level transport, overlap, and failures, **including negative results**. Numerical screens require each local holdout/tangency/drift/anchor/phase-shift relative defect below `1e-6`, plus gauge-free local-window maximum normal angle below `5°` and normalized-coordinate maximum level offset below `0.01`. These overlap thresholds are explicitly *diagnostic*, not physical or rigorous. No numerical screen is promoted to a physical invariant certificate; absence of a pass does not demonstrate nonexistence outside the tested dictionary.

## Execute on the original Linux server

```bash
cd /root/elab1/hysteresis
unzip q550_kick203_cofactor_selection_surface_return_v18_33_bundle.zip
cd q550_kick203_cofactor_selection_surface_return_v18_33_bundle
bash scripts/run_on_server.sh 2>&1 | tee v18_33_server.log
```

For a different pinned model root: `bash scripts/run_on_server.sh --base-root /absolute/pinned/model/root`.

The server performs original Q550 integrations only **after** preflight, then writes the plots, builds the manifest and creates:

`/root/elab1/hysteresis/q550_kick203_cofactor_selection_surface_return_v18_33_sendback.zip`

The audit does **not** regenerate the original 400 orbit periods. The experiment is more computationally expensive than the offline preflight due to the 40 fits and local transport/overlap tests, but prior nonlinear trajectories and nested genealogy are not recomputed.

## Offline preflight (no original server integrations)

```bash
bash scripts/run_preflight.sh
```

Runs 16 synthetic tests, authenticates the original v18.32 parent and re-ranks the archived v18.32 training scores. The output `results/frozen_preflight_v18_33.json` has status `AUTHENTICATED_V18_32_ONLY_NO_NEW_Q550_RUN` and MUST NOT be reported as an original v18.33 Q550 result. The sendback packager refuses to package that alone.

## Server output files

- `results/original_v18_33_proof.json` — complete audit provenance, accepted/rejected candidates, posture/phase/transport diagnostics and explicit limits.
- `results/original_v18_33_selection_scan.csv` — training normalized residuals for all 40 models, old singular objectives and selection flags.
- `results/original_v18_33_surface_retests.json` — shortlisted candidate coefficients, original state center/scales, gauge-free diagnostics, and independent results.
- `results/original_v18_33_posture_overlap.csv` — local training-only window fits compared at exactly the same anchors, with angles and diagnostic level offsets.
- `results/original_v18_33_clock_return.csv` — 0.25/0.5/1.0-xi original local transports, cofactor-predicted level values, phase turns and material displacement.
- `results/original_v18_33_selection_vs_holdout.png` and `results/original_v18_33_surface_return.png` — plot generation scripts included.
- `SHA256SUMS_OUTPUT.json` — complete deterministic manifest.

## Interpretation boundary

The test explores a finite polynomial/phase dictionary and a local 11D Q550 neighborhood with a declared but **nonprivileged normalized-coordinate diagnostic metric**. An overlap-normal angle is not a material torsion observable; a clock return is not an orbit closure; a fitted cofactor relation on finitely sampled states is not a certified invariant hypersurface. No physically admissible constraint has been supplied. The acceptance criterion is a *numerical local screening condition* only, never a rigorous bound over an open neighborhood or a global return certificate.
