# Remaining Risks

## Risks

- The self-management charter is not an implementation of
  RootAuthorityManifest, RepoLayoutInventory, DocTruthReconciler,
  OKFKnowledgeDriftReport, GeneratedOutputLedger, QueueHealthReport, or
  StructureTransaction.
- AIDE_SELF_PROFILE is proposed doctrine only; `.aide/profile.yaml` is not
  changed by this task.
- Generated-output provenance and docs/knowledge/queue drift remain future
  report-only work.
- `.aide/reports` remains flat and high-risk for migration.
- Any future mutation must use separate no-apply maps, validation, review gates,
  and apply authority.

## Recommended Next Gate

`AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
