# Read-only next-plan validation

- Date: 2026-09-29
- WorkUnit: `AIDE-TASK-OS-STATUS-REPAIR-01`
- Changed paths: this evidence, `ExecPlan.md`, `.aide/scripts/aide_lite.py`, and `.aide/scripts/tests/test_x_os_01_task_os_commands.py`.
- Red result: the new test failed because the parser had no `write_report` field.
- Green result: `py -3 -m unittest discover -s .aide/scripts/tests -p test_x_os_01_task_os_commands.py` passed 12/12, with process-local `TEMP` and `TMP` set to the approved D scratch root.
- Compatibility result: `py -3 -m unittest discover -s .aide/scripts/tests -p test_x_os_00_task_os.py` passed 9/9 under the same process-local temporary root. An earlier typo in the filename pattern ran zero tests and supplied no evidence.
- Structural checks: Python AST and `git diff --check` passed.
- Actual queue: `task next-plan` returned `Review current AIDE queue WorkUnits`, `non_mutating: true`, and `lifecycle_apply_authorized: false`. SHA-256 of the tracked next-plan report was unchanged before and after the command.

Default inspection does not write the tracked report. `--write-report` and the
existing direct writer retain explicit generation. This does not qualify the
frozen ZIP, authorize lifecycle apply, or establish a new campaign priority.
