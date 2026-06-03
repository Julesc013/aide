# Remaining Risks

Task: `AIDE-APPLY-02-REPAIR-01`

## Remaining Review Risks

- `AIDE-APPLY-02` still requires `AIDE-CHECK-APPLY-02-RECHECK-01` before acceptance.
- `AIDE-CHECK-APPLY-02` remains the source checkpoint with `NEEDS_REPAIR`; this repair records fixes but does not self-accept the checkpoint.
- The scoped transaction executor remains review-gated and must not be promoted to accepted, production-ready, release-ready, target-repo-capable, or broad active-repo apply capable by this task.

## Remaining Design Limits

- Multi-mutating apply is blocked in v0 with `BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC`; this repair does not implement multi-file atomic transactions.
- Apply mode remains limited to explicit scoped plans and explicit allowed paths.
- No install, upgrade, lifecycle repair, rollback/uninstall, target repository, branch/worktree, release, GitHub, provider/model, Gateway, network, or broad active-repo apply capability is implemented.

## Validation Warnings

- Repo-wide `py -3 .aide/scripts/aide_lite.py validate` failed on a generated-report self-reference issue outside the four authorized checkpoint findings. Dedicated managed-section and transaction fixture validation commands pass after restoring the generated fixture reports.
- PyYAML is unavailable, so YAML parsing was not run with PyYAML. Queue YAML was structurally exercised through AIDE Lite task commands.
- Stale Task OS surfaces remain as pre-existing review-gated surfaces; this repair did not widen into Task OS cleanup.
