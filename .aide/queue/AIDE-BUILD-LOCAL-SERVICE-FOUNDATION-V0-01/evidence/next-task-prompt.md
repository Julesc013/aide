# Next Task Prompt

```text
Create and process AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01.

Independently verify AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01 without repairing
implementation.

Verify local state remains ignored, migrations are deterministic and
idempotent, future migration is refused, object/event writes are atomic,
resource-version conflicts fail closed, events are monotonic with at-least-once
delivery only, cursor resume works, idempotency works, payloads are persisted
before metadata, path containment holds, restart persistence works, corruption
is refused, no network/scheduler/worker/model/provider/trust-enforcement/MCP/
Workbench behavior exists, source checkout is unchanged, tests and broad
validation pass, and reports contain no local path or secret leakage.

If findings remain, recommend exactly:
AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-REPAIR-01

If pass, recommend exactly:
AIDE-ACCEPT-LOCAL-SERVICE-FOUNDATION-V0-01
```
