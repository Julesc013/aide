# Validation

Result: PASS_WITH_WARNINGS.

- Preflight report: `.aide/reports/workunit-cli-mutation-check/preflight.json`, PASS.
- Behavior report: `.aide/reports/workunit-cli-mutation-check/behavior-results.json`, PASS.
- Check report: `.aide/reports/workunit-cli-mutation-check/check-report.json`, PASS_WITH_WARNINGS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.

Warning: a nested Python-runner diagnostic resolved nested `py -3` subprocesses to Python 3.9 and failed on `Path.write_text(newline=...)`; direct shell `py -3` is Python 3.14.5 and all required direct validation passed.
