# Validation

Repair validation run:

```text
py -3 -m py_compile core/execution/local_process_host.py .aide/fixtures/local-process-execution-host/reference_worker.py .aide/scripts/tests/test_aide_local_process_execution_host.py
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
PASS

py -3 .aide/scripts/aide_lite.py local-process-execution-host run
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
PASS_WITH_WARNINGS

py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01
PASS, missing_evidence: 0

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01
PASS, missing_evidence: 0

py -3 -m compileall core/execution .aide/scripts/tests
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_registered_process*.py"
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_execution_host*.py"
PASS

py -3 .aide/scripts/aide_lite.py validate
PASS

git diff --check
PASS

git diff --cached --check
PASS

absolute-path scan over local-process reports and task evidence
PASS

secret-like scan over local-process reports and task evidence
PASS
```

`py -3 .aide/scripts/aide_lite.py commit check --latest` was run before the
new commit exists and passed against the previous commit message; it is rerun
after the repair commit.
