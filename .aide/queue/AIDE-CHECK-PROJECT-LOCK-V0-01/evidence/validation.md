# Validation

Commands run:

- `git status --short --branch`
- `git rev-parse HEAD`
- `git log -8 --oneline`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-PROJECT-LOCK-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-PROJECT-LOCK-V0-01`
- check-local digest, fixture, component, CLI, and non-capability probe
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_project_lock_v0.py"`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-PROJECT-LOCK-V0-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-PROJECT-LOCK-V0-01`
- `git diff --check`
- `git diff --cached --check`

Results:

- Source build task inspection passed with `missing_evidence: 0`.
- Check-local probe found no material ProjectLock defects.
- Focused ProjectLock tests passed: `10` tests.
- Broad AIDE validation passed.
- Check task inspection passed with `missing_evidence: 0`.
- Diff checks passed before staging.

Commit-policy check is recorded after this check packet is committed.
