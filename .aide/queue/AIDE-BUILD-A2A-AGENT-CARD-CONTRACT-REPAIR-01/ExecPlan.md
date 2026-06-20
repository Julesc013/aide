# ExecPlan: AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01

## Objective

Repair the eight material findings from `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01` while preserving the failed check as historical evidence and avoiding live A2A behavior.

## Scope

Allowed changes are limited to the A2A contract helper/schema/tests, regenerated A2A contract artifacts and reports, this repair task packet/evidence, repair reports, queue index, `PLANS.md`, and `IMPLEMENT.md`.

## Milestones

- Verify source chain and failed-check findings.
- Repair official AgentCard shape and metadata separation.
- Harden validation and focused tests.
- Regenerate affected A2A contract artifacts and reports.
- Record evidence, validation, warnings, and next task.

## Review Gate

Stop at `needs_review` and recommend `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01` only.
