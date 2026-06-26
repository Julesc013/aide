# Object Responsibility Map

## DistributionManifest

Defines distribution identity, components, artifacts, digests, protocol ranges, provenance references, local bundle expectations, and release-channel metadata. It does not select target state or authorize publication.

## ProjectLock

Defines a target-owned accepted distribution selection and selected component binding. It does not prove install truth, ownership, or apply authority.

## OwnershipLedger

Defines target path and managed-section ownership classification and preservation metadata. It does not grant install, update, migration, rollback, uninstall, target scan, canary, or public release authority.

## InstallRecord

Will record observed or completed install state, source distribution refs, selected lock refs, ownership ledger refs, installed entry refs, validation refs, evidence refs, warnings, and explicit non-capabilities. It must not perform install apply.

## MigrationRecord

Will record schema or protocol migration decisions, field mapping, unknown-field disposition, manual review, risk, validation, rollback requirements, and evidence. It must not perform migration apply.

## UpdatePlan

Will define a dry-run, reviewable update plan with candidate locks, ownership classifications, planned operations, preservation decisions, conflicts, validation plan, rollback requirements, risk, approval requirements, and evidence. It must not apply the update.

## RollbackBundle

Will record preimages, prior locks, prior install records, reverse operations, validation plans, integrity checks, limitations, and evidence. It must not perform rollback apply.

## UpdateReceipt

Will record what happened after a future reviewed execution path, including operations attempted or skipped, lock transitions, digest changes, validation results, approval refs, warnings, limitations, rollback refs, and evidence. It must not authorize or perform execution.

## DistributionApplyEngine

Will start as fixture-only and temp-workspace-only. It may prove managed file and managed-section operations, preservation, refusal behavior, receipt generation, rollback bundle generation, and rollback verification in fixtures only.

## Self-Consumer Fixture

Will prove AIDE can install, update, roll back, and uninstall itself in a disposable fixture without touching the source repo or real targets.

## Canary Profiles

Will prepare ScreenSave, Eureka, and Dominium inventory/profile/dry-run evidence. They must not mutate those repositories unless later tasks explicitly authorize it.
