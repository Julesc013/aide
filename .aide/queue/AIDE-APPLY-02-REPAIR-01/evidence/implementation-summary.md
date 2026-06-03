# Implementation Summary

Task: `AIDE-APPLY-02-REPAIR-01`

## Findings Repaired

1. Checked-in dry-run example plan failed with `BLOCKED_PREIMAGE_HASH_MISMATCH`.
   - Recomputed the fixture preimage and postimage hashes.
   - Updated `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`.
   - Added a command-level test that runs the checked-in plan from a temporary repo copy and proves the source fixture is unchanged.

2. Resolved symlink/reparse-point target escape was not proven blocked.
   - Added resolved-path validation for target paths and output paths.
   - Added `BLOCKED_RESOLVED_PATH_ESCAPE` for repo-boundary escapes after resolution.
   - Added prewrite resolved-path revalidation before apply-mode mutation.
   - Added tests for symlink file escape, symlink parent escape, resolved protected target, and the resolved-path predicate.

3. Multi-operation apply partial mutation risk was not bounded.
   - Added v0 fail-closed behavior for apply mode when more than one mutating operation is staged.
   - The executor now returns `BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC` before writing any target file.
   - Multi-operation dry-run/report mode remains allowed and non-mutating.

4. Direct core persisted report omitted its own `report_path`.
   - The executor now assigns `report_path` before serializing the final report.
   - The executor also records `rollback_record_path` before writing the report when rollback output is available.
   - The report schema and tests now cover persisted `report_path`.

## Capability Reality

- The scoped transaction executor remains review-gated.
- The repaired v0 supports explicit scoped transaction plans, dry-run/report mode, single-mutating-operation apply mode, managed-section updates, preimage hash checks, postimage verification, staged-change records, and rollback-compatible records.
- Multi-mutating apply is blocked in v0 instead of pretending to provide atomic multi-file transactions.
- No install apply, upgrade apply, lifecycle repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, or broad active-repo apply was performed or authorized.
