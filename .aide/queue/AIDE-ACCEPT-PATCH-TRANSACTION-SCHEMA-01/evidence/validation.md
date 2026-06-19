# Validation Evidence

Validation is run for this blocked acceptance task to confirm repository health,
evidence completeness, and report parseability.

The acceptance decision is not based on rerunning implementation projections.
It is based on live queue truth:

```text
AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01
result: FAILED_VALIDATION
recommended_next_task: AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01
```

Post-materialization validation results are recorded in the terminal run and
commit evidence for this task.

Observed results:

```text
git diff --check: PASS
git diff --cached --check: PASS
py_compile PatchTransaction files: PASS
focused PatchTransaction unittest discovery: PASS, 22 tests
patch-transaction status: PASS_WITH_WARNINGS
patch-transaction validate: PASS_WITH_WARNINGS
predecessor validators: PASS or PASS_WITH_WARNINGS
task inspect AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01: complete, missing_evidence 0
task evidence AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01: missing none
task inspect AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01: complete, missing_evidence 0
task evidence AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01: missing none
task inspect AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01: complete, missing_evidence 0
task evidence AIDE-ACCEPT-PATCH-TRANSACTION-SCHEMA-01: missing none
py -3 .aide/scripts/aide_lite.py validate: PASS
JSON parsing for PatchTransaction, check, and accept reports: PASS
artifact digest comparison against check evidence: PASS
unsupported patch-transaction apply/approve/execute/rollback: fail closed with exit 2
secret-like scan over changed files: PASS, 0 findings
```

Known generated report churn from predecessor validators was restored before
staging.
