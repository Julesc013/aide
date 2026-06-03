# AIDE-APPLY-02 Readiness

- readiness: READY_FOR_AIDE_APPLY_02_WITH_WARNINGS
- next_task: AIDE-APPLY-02 - Scoped Transaction Executor v0
- may_start: true
- implement_in_this_checkpoint: false

## Allowed Scope

- Explicit allowlist file operations.
- Active-repo transaction executor limited to explicit operator-provided paths.
- Managed-section operations only by default.
- Preimage hash capture before mutation.
- Postimage verification after mutation.
- Ownership and marker-boundary checks.
- Rollback record required for every staged active-repo mutation.
- Temp-dir tests and narrowly scoped fixture active-repo tests if AIDE policy permits.

## Forbidden Scope

- Install apply.
- Upgrade apply.
- Repair apply.
- Rollback/uninstall apply.
- Target repository mutation.
- Broad active-repo patching.
- Delete or move operations.
- Branch/worktree mutation.
- Merge, push, promotion, tag, or release publication.
- GitHub API mutation.
- Provider/model/network calls.
- Gateway forwarding.

## Required Safety Gates

- Operator-provided explicit path allowlist.
- Operation plan and staged-change record before mutation.
- Ownership check and managed-marker validation.
- Preimage hash and rollback record before mutation.
- Postimage hash and validation after mutation.
- Conflict classes block mutation rather than repair silently.
- Dry-run or fixture mode remains available.
- Queue review gate remains active after implementation.

## Expected Outputs

- Queue packet and ExecPlan for AIDE-APPLY-02.
- Scoped transaction executor policy and schemas.
- Tests covering allowed path, rejected path, hash mismatch, marker conflict, rollback-record creation, and postimage verification.
- Reports and evidence proving no target, branch, install, repair, upgrade, rollback/uninstall, release, provider, model, network, or Gateway behavior.

## Validation Commands

- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py managed-section validate`
- `py -3 .aide/scripts/aide_lite.py verify`
- targeted executor unit tests once implemented in AIDE-APPLY-02
- `git diff --check`

## Acceptance Criteria

- Executor is limited to explicit paths and managed-section operations by default.
- Every mutation has preimage, postimage, staged-change, and rollback evidence.
- Ambiguous or unsupported state blocks mutation.
- No install/upgrade/repair/rollback/uninstall apply, target mutation, branch/worktree mutation, release publication, GitHub mutation, provider/model call, network call, or Gateway forwarding is introduced.
