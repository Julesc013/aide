# AIDE-APPLY-02 Readiness

- classification: READY_FOR_AIDE_APPLY_02_WITH_WARNINGS
- next_task: AIDE-APPLY-02 - Scoped Transaction Executor v0
- may_start: true
- implement_now: false

## Allowed Next Scope

- explicit allowlist file operations
- active-repo transaction executor limited to explicit operator-provided paths
- managed-section operations only by default
- preimage hash
- postimage verification
- rollback record required
- ownership and marker-boundary checks
- temp-dir tests and narrowly scoped fixture active-repo tests if allowed by policy

## Forbidden Next Scope

- install apply
- upgrade apply
- repair apply
- rollback/uninstall apply
- target repository mutation
- broad active-repo patching
- delete or move operations
- branch/worktree mutation
- merge/push/promotion
- release publication
- GitHub API mutation
- provider/model/network calls
- Gateway forwarding

## Acceptance Bar

AIDE-APPLY-02 must prove scoped mutation safety before any install, repair, upgrade, rollback, uninstall, or target-repo apply phase is considered.
