# Next Task Prompt

```text
Create and process
AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01.

Repo truth outranks this prompt. Read governing queue policy, accepted
RegisteredProcessExecutionProvider v0 evidence, accepted ExecutionHost contract
evidence, accepted LocalProcessExecutionHost v0 evidence, accepted trust and
authorization contract evidence, PLANS.md, IMPLEMENT.md, and current repository
state before writing anything.

Goal:
Build the smallest local, durable, no-network AIDE Service foundation.

Proposed capability:
local_service_foundation_v0

Use Python standard-library SQLite and filesystem content-addressed storage.
Runtime state must remain ignored under `.aide.local/service/**`; do not commit
live DB or payload files.

Required stores:
- migrations
- objects
- trust-bearing events
- artifact metadata
- idempotency
- subscription cursors

Required behavior:
- initialize and health
- deterministic/idempotent migrations
- future migration refusal
- object put/get/list
- resource-version optimistic concurrency
- atomic object update plus event
- append event with monotonic sequence
- read events after sequence
- cursor acknowledgment
- content-addressed artifact write/read
- digest verification and dedupe
- atomic payload-before-metadata
- idempotency key recording
- conflicting idempotency refusal
- close/reopen persistence
- single-writer boundary
- corruption refusal

Delivery semantics: at-least-once only.

Do not implement network, HTTP, sockets, scheduler, worker execution, capability
execution, trust enforcement, MCP, Workbench, distributed locking,
provider/model calls, preview/apply/rollback, repository mutation, GitHub
mutation, release, or promotion.

Stop at needs_review and recommend exactly:
AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
```
