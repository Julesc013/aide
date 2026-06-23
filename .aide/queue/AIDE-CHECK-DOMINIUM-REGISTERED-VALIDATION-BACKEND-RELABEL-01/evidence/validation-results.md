# Validation Results

Initial check result:

```text
PASS_WITH_WARNINGS
material_finding_count: 0
missing_evidence: 0
recommended_next_task: AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
```

Final command results:

```text
PASS py -3 -m py_compile .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01\evidence\independent_relabel_check.py
PASS py -3 .aide\queue\AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01\evidence\independent_relabel_check.py
PASS py -3 -m py_compile core\interop\dominium\registered_validation_backend.py .aide\scripts\aide_lite.py .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
PASS py -3 .aide\scripts\tests\test_aide_dominium_registered_validation_backend.py
PASS_WITH_WARNINGS py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
PASS py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
PASS py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-BUILD-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
PASS py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
PASS py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-CHECK-DOMINIUM-REGISTERED-VALIDATION-BACKEND-RELABEL-01
PASS local absolute path scan over active relabel-check reports and evidence
PASS secret-like value scan over active relabel-check reports and evidence
PASS py -3 .aide\scripts\aide_lite.py validate
PASS git diff --check
PASS git diff --cached --check
PASS git -C C:\Projects\Dominium\dominium status --short --branch
```

Observed Dominium status remained `## main...origin/main [behind 24]`.

No live Dominium command rerun occurred in this check phase.
