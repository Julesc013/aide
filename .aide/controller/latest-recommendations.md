# AIDE Recommendations

## MODE

- advisory_only: true
- applies_automatically: false
- automatic_prompt_mutation: false
- automatic_policy_mutation: false
- automatic_route_mutation: false

## RECOMMENDATIONS

- ID: REC-PACKET-BUDGET
  - failure_class: packet_too_large
  - evidence_source: `.aide/reports/token-savings-summary.md`
  - expected_benefit: Lower prompt cost while keeping compact packets inside configured budgets.
  - risk_level: medium
  - next_action: Tighten context refs, rerun `context`, `pack`, and `review-pack`, then confirm budgets and golden tasks.
  - rollback_condition: Affected packet returns within budget and golden tasks remain PASS.
  - applies_automatically: false

## SAFETY

- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false
