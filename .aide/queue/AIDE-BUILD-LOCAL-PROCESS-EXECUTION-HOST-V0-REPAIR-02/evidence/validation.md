# Validation

Commands run:

```text
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
py -3 .aide/scripts/aide_lite.py local-process-execution-host run
py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-02
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_registered_process*.py"
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_execution_host*.py"
py -3 -m compileall core/execution .aide/scripts/tests
py -3 .aide/scripts/aide_lite.py validate
git diff --check
absolute local path scan over task evidence and local-process reports
secret-like scan over task evidence and local-process reports
```

Initial focused run exposed final symlink classification as path escape. The
implementation was corrected to classify symlinks before existence checks.

Current observed results:

- focused LocalProcessExecutionHost tests: `PASS`;
- live local-process fixture run: `PASS_WITH_WARNINGS`;
- local-process report validation: `PASS_WITH_WARNINGS`, `error_count: 0`;
- task inspect/evidence: `PASS`, `missing_evidence: 0`;
- registered-process and ExecutionHost regressions: `PASS`;
- compileall: `PASS`;
- broad validation: `PASS`;
- diff check: `PASS`;
- absolute local path scan: `PASS`;
- secret-like scan: `PASS`;
- material finding count: `0`;
- missing evidence: `0`.

Additional broad validation is recorded after the full validation pass.
