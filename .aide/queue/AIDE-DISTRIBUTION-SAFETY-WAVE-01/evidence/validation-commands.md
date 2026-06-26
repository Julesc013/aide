# Validation Commands

Planned and executed validation:

- JSON parse for generated wave reports.
- YAML parse using the local available parser when present, with fallback structural text checks.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-DISTRIBUTION-SAFETY-WAVE-01`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-DISTRIBUTION-SAFETY-WAVE-01`.
- `py -3 .aide/scripts/aide_lite.py validate`.
- strict generated-artifact scans for local absolute paths.
- strict generated-artifact scans for secret-like material.
- strict generated-artifact scans for source-output misuse.
- `git diff --check`.
- `git diff --cached --check`.
- `py -3 .aide/scripts/aide_lite.py commit check --latest` after commit.
