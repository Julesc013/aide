# Scoped Transaction Executor

`AIDE-APPLY-02` implements a scoped transaction executor v0. The executor accepts explicit JSON transaction plans, validates explicit allowed paths and protected paths, rejects unsupported or forbidden operations, computes preimage hash values before scoped mutation, verifies postimage verification expectations, writes staged-change records, writes rollback-compatible records, and produces final evidence reports.

The default operation class is `update_managed_section`. It integrates with `core.apply.managed_sections` so generated-section marker parsing, duplicate marker detection, malformed marker detection, nested marker detection, and manual content preservation reuse the existing managed-section patcher.

Supported modes are `dry-run`, `report`, and explicit `apply`. Dry-run/report mode writes report evidence but does not mutate target files. Apply mode is available only when the transaction plan explicitly requests `mode: apply`; it still fails closed on path, operation, marker, preimage hash, postimage verification, staged-change, or rollback-compatible record failures before writing.

This is not production-ready broad active-repo apply. It does not authorize install apply, upgrade apply, repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, broad deletes, or broad moves. The queue status remains review-gated at `needs_review` until `AIDE-CHECK-APPLY-02` reviews the implementation and evidence.
