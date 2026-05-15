# Command Surface Audit

| Family | Available | Validate/status command | Result | Generated outputs | No-apply safe | Target-safe | Warnings |
|---|---|---|---|---|---|---|---|
| core | yes | doctor/validate/test/selftest/eval | PASS | eval and context reports | yes | yes | harness has generated-manifest warning |
| intent | yes | intent validate/status | PASS | latest intent packet/workunit draft | yes | yes | compile output generated during audit |
| repo | yes | repo validate/status | WARN/PASS | repo intelligence maps | yes | yes | unknown classifications advisory |
| quality | yes | quality validate/status | PASS | quality ledger/reports | yes | yes | high advisory warning count |
| refactor | yes | refactor validate/dry-run | PASS | dry-run/map reports | yes | yes | no apply |
| roots | yes | roots validate/status | PASS | root inventory/classification | yes | yes | unknown roots advisory |
| tools | yes | tools validate/status | PASS | tool inventory | yes | yes | execution disabled |
| install | yes | install validate/status | PASS | observe/plan/dry-run/conflict reports | yes | yes | dry-run only |
| repair | yes | repair validate/status | PASS | observe/diagnose/plan/dry-run reports | yes | yes | dry-run only |
| upgrade | yes | upgrade validate/status | PASS | observe/compare/plan/dry-run reports | yes | yes | dry-run only |
| rollback | yes | rollback validate/status | PASS | observe/plan/dry-run reports | yes | yes | dry-run only |
| uninstall | yes | uninstall validate/status | PASS | observe/plan/dry-run reports | yes | yes | dry-run only |
| release | yes | release validate/status/assets/manifest/checksums/provenance/clean | PASS | local bundle reports | yes | yes | no publish |
| release draft | yes | draft-validate/status/upload-plan/checklist/publication-boundary | PASS | local draft and checklist | yes | yes | no publish/upload/tag |
| git | yes | git detect/status/policy/plan and dry-run helpers | PASS/WARN | git helper reports | yes | yes | dirty tree during audit; dev absent |
| changelog | yes | preview/validate/status | PASS | preview release notes/changelog | yes | yes | malformed historical commits recorded |
| github | yes | validate/advisory/status/protection/ci | PASS | advisory reports | yes | yes | report-only; no API mutation |

## Boundary

No command run by QCHECK performed a provider call, model call, GitHub API mutation, branch mutation, tag creation, release creation, upload, target install, or apply action.
