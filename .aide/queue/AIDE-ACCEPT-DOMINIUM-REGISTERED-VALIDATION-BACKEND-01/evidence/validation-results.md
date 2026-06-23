# Validation Results

Initial acceptance result:

```text
ACCEPTED_WITH_WARNINGS
accepted_capability: dominium_registered_validation_command_boundary_invocation_v0
material_finding_count: 0
missing_evidence: 0
recommended_next_task: AIDE-BUILD-REGISTERED-PROCESS-EXECUTION-PROVIDER-V0-01
```

Final command results:

```text
PASS py -3 -m json.tool .aide\reports\dominium-registered-validation-backend-accept\acceptance-report.json
PASS py -3 -m json.tool .aide\reports\dominium-registered-validation-backend-accept\accepted-capability.json
PASS py -3 .aide\scripts\aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
PASS py -3 .aide\scripts\aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-REGISTERED-VALIDATION-BACKEND-01
PASS_WITH_WARNINGS py -3 .aide\scripts\aide_lite.py dominium-registered-validation validate
PASS py -3 .aide\scripts\aide_lite.py validate
PASS local absolute path scan over acceptance reports and evidence
PASS secret-like value scan over acceptance reports and evidence
PASS git -C <dominium-root> status --short --branch
PASS git diff --check
PASS git diff --cached --check
```

Observed Dominium status remained `## main...origin/main [behind 24]`.

No live Dominium command rerun occurred in this acceptance phase.
