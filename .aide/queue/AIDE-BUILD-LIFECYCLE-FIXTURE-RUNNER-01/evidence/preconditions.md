# Preconditions

| Check | Result | Evidence | Notes |
| --- | --- | --- | --- |
| WorkUnit has explicit implementation authority | PASS | `task.yaml` includes `authorizes_implementation: true` | Scope is `lifecycle-fixture-temp-runner-only`. |
| Selected scenario is narrow | PASS | `selected_scenario: install-managed-section` | No other scenario is authorized. |
| Selected mode is temp-only | PASS | `selected_mode: apply-temp` | Canonical fixtures must remain read-only. |
| Existing generated plan exists | PASS | `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json` | Read-only input. |
| Existing expected state exists | PASS | `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/**` | Read-only input. |
| Existing rollback record exists | PASS | `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json` | Read-only input. |

No provider/model/Gateway/network calls, branch/worktree mutation, target repo mutation, release behavior, or broad kernel scaffold is authorized.
