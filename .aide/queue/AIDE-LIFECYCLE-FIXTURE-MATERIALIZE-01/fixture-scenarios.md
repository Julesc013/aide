# Fixture Scenarios

| Scenario | Lifecycle phase | Materialized | Expected status | Expected blocker | Mutation state |
| --- | --- | --- | --- | --- | --- |
| `install-clean` | install | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `install-existing-manual-preserved` | install | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `install-managed-section` | install | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `upgrade-v2` | upgrade | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `upgrade-manual-preserved` | upgrade | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `drift-detected` | upgrade | yes | `BLOCKED` | `BLOCKED_DRIFT_DETECTED` | blocked, no mutation |
| `repair-plan-missing-marker` | repair | yes | `BLOCKED` | `BLOCKED_MARKER_MISSING` | blocked, no mutation |
| `repair-plan-malformed-marker` | repair | yes | `BLOCKED` | `BLOCKED_MARKER_MALFORMED` | blocked, no mutation |
| `rollback-record-generated` | rollback | yes | `PASS_WITH_WARNINGS` | none | static record only |
| `uninstall-manual-preserved` | uninstall | yes | `PASS_WITH_WARNINGS` | none | static fixture only |
| `protected-path-blocked` | install | yes | `BLOCKED` | `BLOCKED_PROTECTED_PATH` | blocked, no mutation |
| `traversal-blocked` | install | yes | `BLOCKED` | `BLOCKED_PATH_TRAVERSAL` | blocked, no mutation |
| `broad-delete-blocked` | uninstall | yes | `BLOCKED` | `BLOCKED_BROAD_DELETE` | blocked, no mutation |

The canonical machine-readable scenario metadata is `.aide/examples/apply/lifecycle-fixtures/scenarios.json`.
