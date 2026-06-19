# Validation Evidence

Validation results:

- `git status --short --branch`: passed; only blocked-check allowed paths changed.
- `git diff --check`: passed; emitted the existing `.aide/queue/index.yaml` CRLF warning.
- `git diff --cached --check`: passed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`: passed; classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-ADAPTER-MANIFEST-01`: passed; no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`: passed; classification `complete`, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-ADAPTER-MANIFEST-01`: passed; no missing evidence.
- JSON parsing for `.aide/reports/adapter-manifest-check/check-report.json`: passed.
- static secret-like value scan over changed files: passed with no value-shaped matches.
- `py -3 .aide/scripts/aide_lite.py validate`: passed.

AdapterManifest compile, unit, status, project, validate, projection, and CLI
probe commands were not run because this check is blocked before source-build
review and those surfaces do not exist.
