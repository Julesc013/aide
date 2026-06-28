# Lifecycle Proofs

Accepted fixture proof coverage:

| Proof | Scenario |
| --- | --- |
| fresh install | `fresh-install` |
| profile generation | `profile-generation` |
| upgrade from previous version | `upgrade-from-previous-version` |
| same-version idempotence | `same-version-idempotence` |
| target-owned-state preservation | `target-owned-state-preservation` |
| rollback | `rollback-after-upgrade` |
| uninstall | `uninstall-preserves-target-state` |
| offline operation | `offline-operation` |
| source repo not target | `source-repo-confusion-refusal` |

These are fixture records, not real target apply behavior.
