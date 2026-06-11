# Preconditions

| Check | Result | Evidence |
| --- | --- | --- |
| Apply gate exists | PASS | `AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01` |
| Gate selected scenario | PASS | `install-managed-section` |
| Gate selected future candidate | PASS | `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01` |
| Gate recorded no execution authority | PASS | `apply_authorized_by_this_gate: false` |
| Blocked apply task exists | PASS | `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01` |
| Blocked apply task mutated no fixture files | PASS | blocker evidence and no changed fixture target paths |
| Install dry-run checkpoint accepted | PASS_WITH_NOTES | `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01` |
| Expected report exists | PASS | `install-managed-section.report.json` |
| Target baseline exists | PASS | target file exists |
| Expected postimage exists | PASS | expected file exists |
| Current preimage hash matches | PASS | `sha256:04b683842eb774461d371a2d2cde8ec101fa13c0fd75fcddb7b98b4944e89b60` |
| Expected postimage hash matches | PASS | `sha256:10adf6b8c183ad0ec69d278ef6173707eeb0925d9796968a6dd9c28c46d80a4b` |
| Rollback record exists | PASS | `install-managed-section.rollback.json` |
| Rollback record check accepted | PASS_WITH_NOTES | `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01` |
| Scoped executor accepted | PASS_WITH_NOTES | `AIDE-CHECK-APPLY-02-RECHECK-01` |
| One mutating operation only | PASS | generated plan has one `update_managed_section` operation |
| Active repo apply required | PASS | not required |
| Target repo apply required | PASS | not required |
| Branch/worktree mutation required | PASS | not required |
| Network/GitHub/provider/Gateway required | PASS | not required |
| Repo validation passes | PASS | validation evidence |
| Worktree clean before task | PASS | preflight status |
| Authority output paths authorized | PASS | task allowlist |
