# Validation

Validation run for `AIDE-CHECK-INTEROP-EXPORTS-01`:

- `git status --short --branch`: PASS; branch `main`.
- `git diff --check`: PASS with the existing line-ending warning for
  `.aide/queue/index.yaml`.
- `git diff --cached --check`: PASS.
- Independent preview hash recomputation: PASS for all six preview artifacts.
- JSON parsing for preview, build report, and check report JSON: PASS.
- Manifest/report consistency: PASS.
- Boundary text scan: PASS; preview files retain queue-authority and
  preview-only/non-capability wording.
- Build artifact immutability check: PASS; `.aide/interop/exports/**` and
  `.aide/reports/interop-exports/**` unchanged from `HEAD`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-INTEROP-EXPORTS-01`:
  PASS; `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-INTEROP-EXPORTS-01`:
  PASS; no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-INTEROP-EXPORTS-01`:
  PASS; classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-INTEROP-EXPORTS-01`:
  PASS; no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Secret-like scan over changed files: PASS; `0` findings across `32` files.

Commit-policy validation is recorded after commit.
