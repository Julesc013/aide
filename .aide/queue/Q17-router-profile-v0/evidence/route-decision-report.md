# Q17 Route Decision Report

## Generated Decision

- JSON: `.aide/routing/latest-route-decision.json`
- Markdown: `.aide/routing/latest-route-decision.md`
- Task packet: `.aide/context/latest-task-packet.md`
- Task represented: `Implement Q18 Cache and Local State Boundary`

## Current Route

- task_class: `architecture_decision`
- risk_class: `governance`
- route_class: `frontier`
- fallback_route_class: `human_review`
- hard_floor_applied: `architecture_decision`
- blocked: `false`
- advisory_only: `true`

## Quality Gate Signals

- token_budget_status: `within_budget`
- verifier_status: `PASS`
- golden_task_status: `PASS`
- outcome_recommendation_status: `PASS`
- quality_gate_status: `PASS`

## Rationale

The generated Q18 packet is about cache and local-state boundaries. Q17 treats
that as an architecture/governance boundary, so the `architecture_decision` hard
floor applies. The route cannot be demoted to `no_model_tool` or a cheap route
solely to save tokens, even though the decision remains advisory and does not
call a model.

## Evidence Sources

- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/controller/latest-outcome-report.md`
- `.aide/controller/latest-recommendations.md`
- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/models/hard-floors.yaml`
- `.aide/models/routes.yaml`
- `.aide/policies/routing.yaml`
- `.aide/reports/token-savings-summary.md`
- `.aide/verification/latest-verification-report.md`

## Token Impact

- Latest Q18 task packet: 3486 chars / 872 approximate tokens
- Root-history baseline in token summary: 54575 approximate tokens
- Estimated task-packet reduction: 98.4%
- Method: chars divided by 4, rounded up

This is not exact provider billing and does not count hidden reasoning,
provider-specific tokenization, cache behavior, or review quality. Q15 golden
tasks and Q12 verification preserve the local quality floor.
