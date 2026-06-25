# Compatibility Map Review

The plan preserves Q43-Q48 as the v0 compatibility foundation.

| Existing surface | v1 treatment |
| --- | --- |
| Q43 install observation | Retain; promote selected fields into v1 observation inputs. |
| Q43 install plan/dry-run | Retain as v0 planning evidence; v1 UpdatePlan supersedes only after accepted. |
| Q43 ownership ledger example | Promote into `OwnershipLedger v1` with migration from old classes. |
| Q44 repair diagnosis/plan | Retain; use as advisory repair evidence and refusal input. |
| Q45 current/source observations | Retain; promote into UpdatePlan input model. |
| Q45 upgrade comparison | Retain; map compatibility findings into v1 plan diagnostics. |
| Q45 upgrade plan/dry-run | Retain as no-apply v0 evidence; v1 UpdatePlan is a new immutable plan contract. |
| Q46 rollback plan | Retain; superseded for update reversal by `RollbackBundle v0` only after accepted. |
| Q46 uninstall plan | Retain; not part of initial v1 update apply path. |
| Q47 release bundle | Retain; source input for `DistributionManifest v1`. |
| Q48 release draft | Retain as publication review evidence; not distribution truth. |

No existing generated `latest-*` output becomes target truth.
