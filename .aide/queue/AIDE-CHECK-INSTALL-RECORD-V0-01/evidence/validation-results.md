# Validation Results

Initial validation for the checked build task passed before this check packet was written.

Check-task validation result: PASS_WITH_WARNINGS.

- JSON parse: PASS
- compileall: PASS
- focused InstallRecord tests: PASS
- `install-record status`: PASS_WITH_WARNINGS
- `install-record project`: PASS_WITH_WARNINGS
- `install-record validate`: PASS_WITH_WARNINGS
- predecessor regression validation: PASS
- Q43-Q48 no-apply/no-publish validators: PASS
- broad AIDE validation: PASS
- build task inspect/evidence: PASS
- check task inspect/evidence: PASS after required `validation.md` evidence was added
- safety scans: PASS
- Git whitespace checks: pending final run before commit
- commit check: pending final run after commit
