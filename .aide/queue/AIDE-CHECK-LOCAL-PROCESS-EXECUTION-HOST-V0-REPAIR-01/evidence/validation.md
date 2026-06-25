# Validation

```text
$env:PYTHONDONTWRITEBYTECODE='1'; py -3 .aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01/evidence/check_local_process_host_repair.py
PASS as check execution; result: REQUEST_CHANGES; material_finding_count: 7; missing_evidence: 0

py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01
PASS; missing_evidence: 0

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01
PASS; missing_evidence: 0

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_local_process_execution_host.py"
PASS

py -3 .aide/scripts/aide_lite.py local-process-execution-host validate
PASS_WITH_WARNINGS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_registered_process*.py"
PASS

py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_execution_host*.py"
PASS

py -3 -m compileall core/execution .aide/scripts/tests .aide/queue/AIDE-CHECK-LOCAL-PROCESS-EXECUTION-HOST-V0-REPAIR-01/evidence
PASS

py -3 .aide/scripts/aide_lite.py validate
PASS

git diff --check
PASS

absolute-path scan over check reports and task evidence
PASS

secret-like scan over check reports and task evidence
PASS
```
