# Validation Results

- Focused LocalProcessExecutionHost tests: `PASS`.
- Live local-process fixture run: `PASS_WITH_WARNINGS`.
- Local-process report validation: `PASS_WITH_WARNINGS`, `error_count: 0`.
- Task inspect: `classification: complete`, `missing_evidence: 0`.
- Task evidence: no missing evidence.
- Registered-process regression tests: `PASS`.
- ExecutionHost contract regression tests: `PASS`.
- Compileall: `PASS`.
- Broad AIDE validation: `PASS`.
- `git diff --check`: `PASS`.
- Absolute local path scan: `PASS`.
- Secret-like scan: `PASS`.
- Repair report: `PASS_WITH_WARNINGS`.
- Material finding count: `0`.
- Missing evidence: `0`.

One initial focused test run failed on final symlink classification. The code
was corrected and the focused suite was rerun successfully.
