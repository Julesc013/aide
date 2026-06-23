# Validation Results

- `py_compile`: PASS
- focused fake-runner unit tests: PASS, 7 tests
- live `dominium-registered-validation run`: one Dominium CLI process spawned; wrapper exited nonzero because generated markdown companions were written after the first validation pass
- report-only `dominium-registered-validation validate`: PASS_WITH_WARNINGS, `error_count: 0`
- strict local-path and secret-like scan: PASS, `findings: 0`
- Dominium status after invocation: clean local `main`, behind `origin/main` by 24 local observations
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- compileall for Dominium interop, core protocol, and AIDE script tests: PASS
- broad `aide_lite.py validate`: PASS
