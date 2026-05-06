# AIDE Recommendations

## MODE

- advisory_only: true
- applies_automatically: false
- automatic_prompt_mutation: false
- automatic_policy_mutation: false
- automatic_route_mutation: false

## RECOMMENDATIONS

- ID: REC-PROCEED-Q18-WITH-GATES
  - failure_class: unknown
  - evidence_source: `.aide/controller/latest-outcome-report.md`
  - expected_benefit: Define cache and local-state boundaries after routing is advisory and local quality gates are healthy.
  - risk_level: low
  - next_action: Proceed to Q18 Cache and Local State Boundary as a repo-local boundary phase only; do not call providers or implement Gateway.
  - rollback_condition: If any verifier, golden-task, route, token, or controller signal regresses, pause Q18 and repair the failing local gate first.
  - applies_automatically: false

## SAFETY

- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false
