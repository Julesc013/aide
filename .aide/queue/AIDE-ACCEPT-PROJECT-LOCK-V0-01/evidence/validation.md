# Validation

Commands run before acceptance materialization:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-PROJECT-LOCK-V0-01`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-PROJECT-LOCK-V0-01`
- ProjectLock check report inspection
- `git status --short --branch`

Final validation after materialization:

- `py -3 .aide/scripts/aide_lite.py project-lock validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-PROJECT-LOCK-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-PROJECT-LOCK-V0-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `git diff --check`
- `git diff --cached --check`

Results:

- ProjectLock validation passed with `PASS_WITH_WARNINGS`.
- Acceptance task inspect/evidence passed with `missing_evidence: 0`.
- Broad AIDE validation passed.
- Diff checks passed.
