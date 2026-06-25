# AIDE-BUILD-LOCAL-SERVICE-FOUNDATION-V0-01

Build the smallest local, durable, no-network AIDE Service foundation.

Proposed capability:

```text
local_service_foundation_v0
```

Use Python standard-library SQLite and filesystem content-addressed storage.
Runtime state remains ignored under `.aide.local/service/**`; do not commit live
DB or payload files.

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

Stop at `needs_review` and recommend exactly:

```text
AIDE-CHECK-LOCAL-SERVICE-FOUNDATION-V0-01
```
