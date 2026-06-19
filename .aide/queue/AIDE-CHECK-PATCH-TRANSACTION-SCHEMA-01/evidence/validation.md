# Validation Evidence

Commands run before report materialization:

```text
git status --short --branch
git diff --check
git diff --cached --check
py -3 -m py_compile core/protocol/patch_transaction.py .aide/scripts/aide_lite.py .aide/scripts/tests/test_aide_patch_transaction.py
py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_patch_transaction.py
py -3 .aide/scripts/aide_lite.py patch-transaction status
py -3 .aide/scripts/aide_lite.py patch-transaction project
py -3 .aide/scripts/aide_lite.py patch-transaction validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py workunit validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py conformance-result validate
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01
```

Focused tests and predecessor validators passed or returned expected
`PASS_WITH_WARNINGS`.

Independent path-scope probes produced `FAILED_VALIDATION` for this check.

Final validation after materializing the check task is recorded by the terminal
run and commit evidence for this queued task.

Post-materialization checks:

```text
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
classification: complete
missing_evidence: 0

py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
missing: none

py -3 .aide/scripts/aide_lite.py validate
status: PASS
```

Generated predecessor-report churn from validators was restored before staging.
