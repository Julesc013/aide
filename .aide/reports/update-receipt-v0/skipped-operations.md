# UpdateReceipt v0 Skipped Operations

Skipped operations are recorded as receipt facts only and do not authorize retry or apply.

| Skipped Operation | Source Operation | Reason | Disposition |
| --- | --- | --- | --- |
| aide://update-receipt/skipped/runtime-generated-local-state | aide://update-plan/operation/runtime-generated-local-state | runtime_generated | recorded_no_apply |
| aide://update-receipt/skipped/project-overlay-policy | aide://update-plan/operation/project-overlay-policy | project_overlay | recorded_no_apply |
| aide://update-receipt/skipped/evidence-only-queue-evidence | aide://update-plan/operation/evidence-only-queue-evidence | evidence_only | recorded_no_apply |
| aide://update-receipt/skipped/never-touch-git | aide://update-plan/operation/never-touch-git | never_touch | recorded_no_apply |
| aide://update-receipt/skipped/project-owned-readme | aide://update-plan/operation/project-owned-readme | project_owned | recorded_no_apply |
| aide://update-receipt/skipped/local-only-operator-state | aide://update-plan/operation/local-only-operator-state | local_only | recorded_no_apply |
| aide://update-receipt/skipped/unknown-unclassified | aide://update-plan/operation/unknown-unclassified | unknown_ownership | recorded_no_apply |
