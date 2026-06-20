# ExecPlan: AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01

## Objective

Independently check the A2A Agent Card contract build against the pinned A2A 1.0 AgentCard field model and AIDE no-runtime boundaries.

## Scope

Check-only. Allowed writes are the task packet/evidence, `.aide/reports/a2a-agent-card-contract-check/**`, `.aide/queue/index.yaml`, `PLANS.md`, and `IMPLEMENT.md`.

## Plan

1. Verify the MCP acceptance and A2A build source chain.
2. Parse generated A2A JSON without importing the production helper.
3. Review protocol version pins, AgentCard required fields, interfaces, provider, capabilities, security, skills, metadata separation, runtime facts, authority boundaries, and determinism.
4. Run focused tests, CLI checks, predecessor validators, task evidence checks, broad validation, JSON parsing, unsupported operation probes, and secret scan.
5. Stop at `needs_review` and recommend `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` because material defects are present.

## Result

`FAILED_VALIDATION` with 8 material findings.
