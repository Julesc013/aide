# AIDE Outcome Report

## RESULT

- result: WARN
- mode: advisory_only
- applies_automatically: false

## SIGNALS

- adapter_guidance: PASS / unknown / info
- context_artifacts: PASS / unknown / info
- golden_tasks: PASS / unknown / info
- review_packet: PASS / unknown / info
- token_ledger: WARN / packet_too_large / warning
- verifier: PASS / unknown / info

## FAILURE_CLASSES

- packet_too_large: 1

## NEXT_ACTION

- top_recommendation: REC-PACKET-BUDGET: Tighten context refs, rerun `context`, `pack`, and `review-pack`, then confirm budgets and golden tasks.
- recommendations: `.aide/controller/latest-recommendations.md`
- outcome_ledger: `.aide/controller/outcome-ledger.jsonl`

## SAFETY

- provider_or_model_calls: none
- network_calls: none
- automatic_mutation: false
- raw_prompt_storage: false
- raw_response_storage: false
- controller_policy: `.aide/policies/controller.yaml`
