# Remaining Risks

## Non-Blocking

- The JSON Schema artifact is not wired into runtime validation. Current
  behavior is safe because helper validation and tests pass, but executable
  schema conformance remains unproven.
- The envelope remains `aide.dev/v1alpha1`; stronger compatibility guarantees
  should wait until schema/helper alignment is hardened.
- The slice covers lifecycle fixture runner reports only. EvidencePacket,
  WorkUnit, TestJob, Checkpoint, PromotionPolicy, Service, Commander, provider,
  branch/worktree, target apply, rollback, and release surfaces remain deferred.

## Next Mitigation

Run `AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` before extracting the
EvidencePacket schema.
