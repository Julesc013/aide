# ExecPlan: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01

## Objective

Independently verify that `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` closes the eight material A2A AgentCard standards-alignment findings without broadening A2A capability.

## Scope

Allowed changes are limited to this check task packet, task-local evidence, `.aide/reports/a2a-agent-card-contract-repair-check/`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Steps

1. Verify source-chain integrity for the A2A build, failed check, and repair.
2. Independently inspect generated AgentCard JSON and repair reports.
3. Verify runtime, publication, registration, delegation, network, provider, worker, mutation, and trust boundaries remain false.
4. Run focused tests, A2A CLI validation, predecessor validators, broad AIDE validation, unsupported command probes, and secret scan.
5. Materialize check reports and evidence, then stop at `needs_review`.

## Exit

Result is `PASS_WITH_WARNINGS`; next task is `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.
