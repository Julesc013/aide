# Lifecycle Matrix

| Scenario | Phase | Expected result | Boundary |
| --- | --- | --- | --- |
| `fresh-install` | fresh install | `PASS_WITH_WARNINGS` | fixture only |
| `profile-generation` | profile generation | `PASS_WITH_WARNINGS` | target-local identity only |
| `upgrade-from-previous-version` | upgrade | `PASS_WITH_WARNINGS` | plan/rollback/receipt refs only |
| `same-version-idempotence` | idempotence | `PASS_WITH_WARNINGS` | no-op update |
| `target-owned-state-preservation` | preservation | `PASS_WITH_WARNINGS` | target-owned state preserved |
| `rollback-after-upgrade` | rollback | `PASS_WITH_WARNINGS` | rollback bundle expected |
| `uninstall-preserves-target-state` | uninstall | `PASS_WITH_WARNINGS` | no blanket `.aide` deletion |
| `offline-operation` | offline | `PASS_WITH_WARNINGS` | no network or provider/model requirement |
| `source-repo-confusion-refusal` | source/target separation | `BLOCKED` | source repo cannot be target |
