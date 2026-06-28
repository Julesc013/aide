# Coverage Matrix

| Required proof | Scenario | Check result |
| --- | --- | --- |
| Fresh install | `fresh-install` | PASS |
| Profile generation | `profile-generation` | PASS |
| Upgrade from previous version | `upgrade-from-previous-version` | PASS |
| Same-version idempotence | `same-version-idempotence` | PASS |
| Target-owned state preservation | `target-owned-state-preservation` | PASS |
| Rollback | `rollback-after-upgrade` | PASS |
| Uninstall and preserve | `uninstall-preserves-target-state` | PASS |
| Offline operation | `offline-operation` | PASS |
| Source repo is not installed target | `source-repo-confusion-refusal` | PASS |

Focused tests and structured JSON review both confirm this coverage.
