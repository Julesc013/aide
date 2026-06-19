# Validation

Completed checks:

- `git status --short --branch`: expected acceptance-only working tree changes.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS before staging.
- JSON parsing for manifest, preview JSON artifacts, build reports, check
  report, and acceptance report: PASS.
- Independent artifact hash recomputation: PASS for all six preview artifacts.
- Manifest path containment validation: PASS.
- Duplicate manifest path and logical identity checks: PASS.
- Manifest/build/check count consistency: PASS.
- Manifest and build report hash consistency: PASS.
- Independent check hash verification evidence reviewed: PASS.
- Bounded Aider YAML structural review: PASS.
- Markdown UTF-8 readability and preview markers: PASS.
- Build/check artifact immutability checks: PASS.
- Forbidden predecessor/protocol/OKF/export/check-report churn scan: PASS.
- Task inspect/evidence for build, check, and acceptance tasks: PASS with
  `missing_evidence: 0`.
- Preview-only, queue-authority, and live-endpoint wording scan: PASS.
- Secret-like scan: PASS with zero findings across 70 checked files.
- Broad `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- Commit-policy validation is recorded after the acceptance commit is created.
