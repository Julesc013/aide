# Validation

Result: validation completed with check result `REQUEST_CHANGES`.

Passed:

- `git rev-parse 1e8889e`
- `git show --no-patch --format=fuller 1e8889e`
- `py -3 -m compileall -q core/interop/dominium core/protocol .aide/scripts/tests`
- `py -3 -u .aide/scripts/tests/test_aide_dominium_readonly_seam.py -v` (`111` tests, passed)
- `py -3 -u .aide/scripts/tests/test_aide_dominium_readonly_seam_repair.py -v` (`20` tests, passed)
- `py -3 -u .aide/scripts/tests/test_aide_dominium_readonly_seam_repair_02.py -v` (`12` tests, passed)
- `py -3 .aide/scripts/aide_lite.py dominium-seam status`
- `py -3 .aide/scripts/aide_lite.py dominium-seam snapshot`
- `py -3 .aide/scripts/aide_lite.py dominium-seam project`
- `py -3 .aide/scripts/aide_lite.py dominium-seam validate`
- `py -3 .aide/scripts/aide_lite.py dominium-seam diff`
- `py -3 .aide/scripts/aide_lite.py dominium-seam demo`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`
- `py -3 .aide/scripts/aide_lite.py validate`
- JSON parsing for check reports and task evidence
- Dominium worktree immutability check
- strict credential-shaped secret scan

Timed out and replaced by narrower successful runs:

- Combined validation batch timed out before writing its summary.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_dominium_readonly_seam*.py"` timed out.
- Parallel individual suite run timed out for the base and Repair 02 suites; no orphaned validation processes were left running after cleanup.

Material check failures are recorded in
`.aide/reports/dominium-readonly-seam-v0-repair-02-check/check-report.json`.
The check remains complete because this is a `REQUEST_CHANGES` task, not an
acceptance gate.
