# Capability Reality

## Current Labels

- install apply: `blocked_planned_only`
- upgrade apply: `blocked_planned_only`
- lifecycle repair apply: `blocked_planned_only`
- rollback apply: `blocked_planned_only`
- uninstall apply: `blocked_planned_only`
- fixture lifecycle apply: `planned`
- active AIDE repo apply: `blocked_pending_gate`
- target repo apply: `deferred_pending_target_authority`
- branch/worktree mutation: `prohibited`
- release/promotion: `prohibited`
- provider/model/Gateway/network support: `deferred_prohibited`

## Evidence

- Q43 install model defines no-apply install observation, plan, and dry-run only.
- Q44 repair/doctor model defines no-apply repair observation, diagnosis, plan, dry-run, and doctor evidence only.
- Q45 upgrade model defines no-apply upgrade observation, compare, plan, dry-run, and validation only.
- Q46 rollback/uninstall model defines no-apply rollback and uninstall observation, plan, dry-run, and validation only.
- Scoped transaction executor v0 is accepted with notes and review-gated. It supports explicit scoped managed-section updates but forbids install, upgrade, repair, rollback/uninstall, target mutation, branch/worktree mutation, release publication, provider/model calls, Gateway calls, network calls, and broad active-repo apply.

## Prohibited Labels

No lifecycle surface is production-ready, release-ready, target-repo capable, broad-apply capable, autonomous, or install/upgrade/repair/rollback/uninstall apply capable.
