# AIDE Recommendations

## MODE

- advisory_only: true
- applies_automatically: false

## RECOMMENDATIONS

- ID: REC-PENDING-CONTROLLER-COMMAND
  - evidence_source: `.aide/controller/README.md`
  - expected_benefit: Generate deterministic recommendations from current local signals.
  - risk_level: low
  - next_action: Run `py -3 .aide/scripts/aide_lite.py optimize suggest`.
  - rollback_condition: No repository behavior changes are applied by the recommendation report.
  - applies_automatically: false

## SAFETY

- provider_or_model_calls: none
- network_calls: none
- automatic_mutation: false
