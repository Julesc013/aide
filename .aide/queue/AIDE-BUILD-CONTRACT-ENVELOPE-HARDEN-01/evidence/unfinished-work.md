# Unfinished Work

## Finished In This Turn

- Schema file is loaded during `contract-envelope validate`.
- Minimal schema subset validation is executed against envelope projections.
- Schema/helper alignment is checked.
- Unknown optional fields are still tolerated.
- Unknown required capabilities still fail closed.

## Partially Finished In This Turn

- JSON Schema validation is intentionally partial and limited to the current
  schema's required/type/property needs.

## Not Attempted By Design

- Full JSON Schema engine.
- EvidencePacket schema.
- WorkUnit schema.
- TestJob schema.
- Checkpoint schema.
- PromotionPolicy schema.
- WorkUnit CLI.
- Test Broker.
- Service.
- Commander.
- provider adapters.
- branch/worktree allocator.
- target repo apply.
- rollback execution.
- release/promotion.
- OpenTelemetry, SARIF, SPDX, CycloneDX, SLSA, in-toto, and OpenAPI.

## Blocked By Repo Policy

- None for this bounded hardening slice.

## Blocked By Missing Files Or Commands

- None observed so far.
