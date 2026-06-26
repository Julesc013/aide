# Dependency Review

The wave starts after three accepted distribution-safety foundation objects:

- `distribution_manifest_v1` accepted by `AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`.
- `project_lock_v0` accepted by `AIDE-ACCEPT-PROJECT-LOCK-V0-01`.
- `ownership_ledger_v1` accepted with warnings by `AIDE-ACCEPT-OWNERSHIP-LEDGER-V1-01`.

The OwnershipLedger downstream-use report allows later objects to cite ownership entries, Q43 dispositions, operation classifications, preimage/digest fields, and final ownership state after a future reviewed apply.

It forbids downstream objects from inferring vendor ownership from path absence, overwriting preservation classes without later reviewed policy, treating source output as target truth, treating Q43 projection as migration apply, or treating acceptance as release, install, update, rollback, uninstall, target scan, canary, or public readiness authority.
