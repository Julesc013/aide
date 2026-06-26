# Remaining Risks

- OwnershipLedger v1 is proposed until independent check and acceptance.
- It records ownership metadata only; it does not prove an apply engine,
  InstallRecord, UpdatePlan, rollback bundle, or target mutation behavior.
- The source repository remains the producer of the reference ledger; target
  repositories must generate target-local ownership ledgers in later apply
  phases.
