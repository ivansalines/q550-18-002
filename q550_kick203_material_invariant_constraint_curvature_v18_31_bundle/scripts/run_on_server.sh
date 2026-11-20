#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
PYTHON=${PYTHON:-python3.13}
command -v "$PYTHON" >/dev/null 2>&1 || PYTHON=python3
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
"$PYTHON" -m unittest discover -s tests -p 'test_material_invariant_v18_31.py' -v
"$PYTHON" scripts/frozen_preflight_v18_31.py
# Resume only when all completed pre-serialization intermediates exist.
# The recovery script independently replays the source samples and checks
# stored selection results before admitting a recovered original proof.
if [[ ! -f results/original_invariant_discovery_proof_v18_31.json    && -f results/original_invariant_candidates_v18_31.csv    && -f results/original_discovered_candidate_coefficients_v18_31.json    && -f results/original_constraint_normal_curvature_v18_31.json    && $# -eq 0 ]]; then
    echo 'v18.31.2: recovering original completed work after JSON serialization error'
    "$PYTHON" scripts/finalize_partial_v18_31_2.py
else
    "$PYTHON" scripts/original_material_invariants_v18_31.py "$@"
fi
"$PYTHON" scripts/plot_v18_31.py
"$PYTHON" scripts/build_manifest.py
"$PYTHON" scripts/pack_sendback.py
