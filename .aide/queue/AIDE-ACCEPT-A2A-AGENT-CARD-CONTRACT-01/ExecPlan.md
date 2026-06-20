# AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01 ExecPlan

## Objective

Accept or reject the repaired `minimal_a2a_agent_card_contract` slice after reviewing the complete MCP acceptance, A2A build, failed independent check, repair, and independent repair-check chain.

## Scope

Allowed changes are limited to this acceptance task packet and evidence, `.aide/reports/a2a-agent-card-contract-accept/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Dependencies

- `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01`: `ACCEPTED_WITH_WARNINGS`, evidence complete.
- `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01`: `PASS_WITH_WARNINGS`, evidence complete.
- `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01`: `FAILED_VALIDATION`, evidence complete and preserved with eight material findings.
- `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01`: `PASS_WITH_WARNINGS`, evidence complete, eight findings repaired.
- `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01`: `PASS_WITH_WARNINGS`, evidence complete, zero material findings, recommends this acceptance task.

## Work Plan

1. Verify the live queue and source-chain task evidence.
2. Inspect the repaired official AgentCard projection, supported interface, candidate-skill separation, runtime facts, and non-capabilities.
3. Confirm the failed check and repair evidence are preserved.
4. Consolidate acceptance scope and warning debt.
5. Materialize acceptance reports and task-local evidence.
6. Run the required validation matrix.
7. Stop at `needs_review` and recommend `AIDE-DOMINIUM-INTEGRATION-CHARTER-01`.

## Non-Goals

No live A2A endpoint, AgentCard publication, agent registration, authentication, authorization, task delegation, worker execution, provider/model/network call, runtime, Host Contract, Dominium Bridge, Workbench, repository mutation, release, or promotion is implemented or authorized.

## Exit Criteria

The task stops at `needs_review` with `ACCEPTED_WITH_WARNINGS`, complete evidence, no unresolved material findings, preserved historical failure evidence, explicit non-capabilities, and exactly one serialized next task recommendation.
