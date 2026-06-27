# Accepted Fail-Closed Model

RollbackBundle v0 is accepted as fail-closed for:

- missing `update_plan_ref`;
- missing `target_project_ref`;
- missing prior ProjectLock;
- missing candidate ProjectLock;
- missing OwnershipLedger;
- missing InstallRecord where required;
- missing preimage artifact;
- preimage digest mismatch;
- candidate distribution mismatch;
- source distribution mismatch;
- reverse operation touching `project_owned` content;
- reverse operation touching `project_overlay` content;
- reverse operation touching `local_only` content;
- reverse operation touching `runtime_generated` content;
- reverse operation touching `evidence_only` content;
- reverse operation touching `never_touch` content;
- reverse operation for unknown ownership;
- reverse operation lacking evidence;
- rollback bundle claiming rollback apply authority;
- rollback bundle claiming install, update, or uninstall authority;
- unknown required feature;
- absolute path;
- path traversal;
- source latest output as target truth;
- target repository mutation claim.

These refusals are validation semantics, not apply behavior.
