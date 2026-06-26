# AIDE-CHECK-OWNERSHIP-LEDGER-V1-01

Repo truth outranks this prompt.

Independently verify `AIDE-BUILD-OWNERSHIP-LEDGER-V1-01` as a check-only task.
Do not repair implementation, do not accept OwnershipLedger v1, and do not begin
InstallRecord.

The check covers schema/helper/projection alignment, ownership class behavior,
file entry model, managed section model, Q43 migration, path and section safety,
conflict behavior, fixture coverage, no-overclaiming, and validation evidence.

If any material finding remains, recommend exactly:

```text
AIDE-BUILD-OWNERSHIP-LEDGER-V1-REPAIR-01
```

If no material finding remains, recommend exactly:

```text
AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01
```

Stop at `needs_review`.
