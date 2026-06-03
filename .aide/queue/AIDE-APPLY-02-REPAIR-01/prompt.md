# AIDE-APPLY-02-REPAIR-01 Prompt

Repair only these AIDE-CHECK-APPLY-02 findings:

1. Checked-in dry-run example plan fails with `BLOCKED_PREIMAGE_HASH_MISMATCH`.
2. Target path checks do not prove resolved symlink/reparse-point targets stay inside allowed bounds.
3. Multi-operation apply can partially mutate if a later write or verification fails.
4. Direct core persisted report can omit its own `report_path`.

This is not lifecycle repair apply. Preserve all install, upgrade, rollback/uninstall, target, branch/worktree, merge, push, promotion, release, GitHub, provider/model, Gateway, network, and broad active-repo apply prohibitions. End at `needs_review`.
