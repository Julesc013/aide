# Accepted Fail-Closed Model

UpdateReceipt v0 fails closed for:

- missing `update_plan_ref`;
- missing `rollback_bundle_ref`;
- missing old or new ProjectLock refs;
- missing target project ref;
- receipt references to operations not present in UpdatePlan;
- receipt claims of unplanned operations;
- changed project-owned, project-overlay, local-only, never-touch, or unknown ownership content;
- preimage digest mismatch;
- postimage digest mismatch;
- missing changed artifact ref;
- missing validation result where required;
- missing approval ref where required;
- missing RollbackBundle ref;
- authorization claims;
- update, install, migration, rollback, repair, or uninstall apply claims;
- target repo mutation claims;
- release readiness claims;
- absolute paths;
- traversal paths;
- source latest output used as target truth;
- unknown required features.
