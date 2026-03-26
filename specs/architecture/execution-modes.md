# Execution Modes

## Why AIDE needs more than one mode

The repository's researched host lanes do not all support the same runtime strategy.

- some lanes can plausibly call shared logic directly
- some lanes need a process boundary because the host contract or implementation language differs
- some lanes fit better as a thin client over a longer-lived broker

AIDE therefore defines stable execution modes while keeping the request and response contracts consistent across them.

## `embedded`

### What it is

The host adapter calls shared logic directly in-process.

### Likely fit

- native host lanes with compatible runtime and packaging constraints
- cases where latency and direct library access matter more than process isolation

### Tradeoffs

- lowest transport overhead
- simplest request and response flow
- strongest coupling to host runtime and ABI constraints

### Risk and complexity

- highest risk of host-runtime entanglement
- harder to isolate crashes or incompatible dependencies
- harder to reuse when a host requires a different language or process model

## `cli-bridge`

### What it is

The host adapter invokes a shared command-line entry point and exchanges request and response payloads through files, standard I/O, or explicit payload arguments.

### Likely fit

- archival or legacy hosts where direct embedding is hard
- hosts that can launch tools but cannot safely embed a shared runtime
- early bootstrapping where a stable protocol is needed before a richer service exists

### Tradeoffs

- simpler than a long-lived service
- process startup overhead on every call
- good auditability and clear failure boundaries

### Risk and complexity

- higher latency than `embedded`
- repeated process creation can be expensive
- state handoff must stay explicit

## `local-service`

### What it is

The host adapter communicates with a local broker, daemon, or service process that owns the shared runtime.

### Likely fit

- companion lanes
- modern out-of-process native contracts
- scenarios where multiple adapters or tools should share one local engine instance

### Tradeoffs

- best process isolation
- better amortized startup cost than `cli-bridge`
- introduces service lifecycle, connectivity, and local coordination complexity

### Risk and complexity

- most operational moving parts
- requires service discovery, health checks, or reconnect behavior
- local protocol stability becomes more important because multiple clients may depend on it

## Stability requirement

Execution mode changes must not change feature semantics. A feature request should mean the same thing whether it flows through `embedded`, `cli-bridge`, or `local-service`.

Only transport, lifecycle, and local runtime behavior should vary by mode.
