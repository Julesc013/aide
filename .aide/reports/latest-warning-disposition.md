# Latest Warning Disposition

## AIDE-CHECK-OS-01

Current classification is `PARTIAL_NEEDS_REPAIR`.

| Class | Count | Disposition |
| --- | ---: | --- |
| harmless | 2 | unsupported exact `test plan`; `summary-validate` requires `--file`. Supported equivalents passed. |
| expected_review_gate | 6 | predecessor and checkpoint tasks remain review-gated. |
| expected_generated_state | 2 | generated reports refreshed; changelog preview malformed history is review-only. |
| expected_dirty_pack_provenance | 2 | pack-status and git plan record dirty checkpoint source before commit. |
| deferred_target_work | 4 | Eureka, Dominium, target sync, and target pilots remain deferred. |
| capability_overclaim_warning | 1 | non-blocking capability wording review. |
| assigned_next | 1 | next task assigned to Task OS report-consistency repair. |
| blocking | 1 | Task OS generated checkpoint/next-plan reports are stale relative to X-OS-02 truth. |
| unknown_needs_review | 0 | none. |

No apply, branch/worktree, target, release, provider/model, network, GitHub API, Gateway, scheduler, or repair execution warning was observed.
