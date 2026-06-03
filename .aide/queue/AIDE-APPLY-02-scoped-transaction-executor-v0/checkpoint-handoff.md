# AIDE-CHECK-APPLY-02 Handoff

`AIDE-CHECK-APPLY-02` is the required checkpoint after future `AIDE-APPLY-02` implementation.

The checkpoint must review:

- live task packet and ExecPlan authority;
- changed files against allowed paths;
- protected paths untouched;
- forbidden operations preserved;
- dry-run/report mode produces no mutation;
- explicit apply mode, if present, is path-bounded and operation-allowlisted;
- preimage hash checks;
- postimage verification;
- rollback-compatible records;
- staged-change records;
- managed-section marker conflict handling;
- manual content preservation;
- evidence and validation completeness;
- capability reality labels;
- unsupported production-ready, release-ready, target-apply, provider/model, Gateway, or network claims.

Allowed checkpoint outputs are review reports, warning disposition, repair recommendations, and the next single task. The checkpoint must not introduce new broad implementation or apply surfaces.
