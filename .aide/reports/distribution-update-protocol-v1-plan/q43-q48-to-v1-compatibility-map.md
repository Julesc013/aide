# Q43-Q48 To v1 Compatibility Map

| Existing surface | Current role | v1 treatment | Notes |
| --- | --- | --- | --- |
| `.aide/install/install-observation.schema.json` | source/target observation | retained unchanged initially | Promoted fields feed install/update observations. |
| `.aide/install/install-plan.schema.json` | no-apply install plan | retained as v0 evidence | Superseded by `UpdatePlan v1` only for reviewed update paths. |
| `.aide/install/ownership-ledger.schema.json` | example ownership ledger | promoted into `OwnershipLedger v1` | Requires taxonomy migration and exact managed-section identity. |
| `.aide/repair/repair-plan.schema.json` | no-apply repair plan | retained as advisory input | Repair findings can refuse or gate updates, not authorize apply. |
| `.aide/upgrade/upgrade-comparison.schema.json` | diff and compatibility | retained as compatibility input | Findings normalize into v1 diagnostics. |
| `.aide/upgrade/upgrade-plan.schema.json` | no-apply upgrade plan | retained as v0 evidence | `UpdatePlan v1` adds immutable approval binding. |
| `.aide/rollback/rollback-plan.schema.json` | no-apply rollback plan | retained as v0 evidence | `RollbackBundle v0` becomes per-update pre-apply recovery bundle. |
| `.aide/uninstall/uninstall-plan.schema.json` | no-apply uninstall plan | retained unchanged initially | Not part of initial update apply path. |
| `.aide/release/release-bundle.schema.json` | local archive bundle | retained as source input | `DistributionManifest v1` references bundle artifacts and digests. |
| `.aide/release/github-release-draft.schema.json` | local draft evidence | retained as publication review material | Not distribution truth and not a publication action. |

Field actions:

- Retain unchanged: no-apply booleans, preservation lists, conflicts, operations,
  verification plans, release artifact hashes, no-publish booleans.
- Promote into v1: distribution identity, component digests, protocol ranges,
  ownership classes, managed-section identifiers, compatibility findings,
  preimage/postimage hashes, rollback prerequisites.
- Rename through migration: older ownership class labels that do not distinguish
  vendor-managed files from vendor-managed sections.
- Deprecate: any field implying automatic migration or apply in Q43-Q48 latest
  outputs.
- Derived only: latest status summaries and Markdown reports.
- Superseded later: no-apply upgrade plan operations once `UpdatePlan v1` is
  accepted for a fixture update path.
