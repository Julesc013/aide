# Validation

The generated report at
`.aide/reports/dominium-workunit-validation-slice/validation.json` currently
records:

- `status: PASS_WITH_WARNINGS`
- `validated: true`
- `required_outputs_present: true`
- `exactly_one_invocation: true`
- `no_mutation: true`
- `validation_errors: []`
- `recommended_next_task: AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`

The invocation report at
`.aide/reports/dominium-workunit-validation-slice/invocation-result.json`
records a typed `DominiumValidationRunResult` with:

- `capability_id: dominium.validation.run`
- `invocation_count: 1`
- `dominium_validation_run_invoked: true`
- `typed_result: true`
- `workspace_mutated: false`
- forbidden boundary fields set to boolean `false`

Additional validation:

- Focused WorkUnit validation slice unit tests passed.
- Broad `aide_lite.py validate` passed.
- Task inspection reports `classification: complete` and `missing_evidence: 0`.
- WorkUnit inspection passed.
- Repair 04 and Repair 05 Dominium seam test modules passed under `unittest discover`.

Historical seam discovery warning:

- The full `test_aide_dominium_readonly_seam*.py` discovery pattern timed out
  under bounded reruns.
- Four older historical seam modules also timed out when run with exact
  discovery patterns.
- Those timeouts are not claimed as passes and should be reviewed separately if
  the independent check requires a full historical-suite rerun.
