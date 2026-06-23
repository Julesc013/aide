# AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Build the first real cross-repository operation after accepting the Dominium
read-only seam.

Authorize exactly one bounded, local, read-only invocation of:

```text
dominium.validation.run
```

against a pinned revision or temporary fixture workspace. The invocation must
flow through:

```text
Dominium context
-> ContextDescriptor
-> ContextPack
-> WorkUnit
-> registered validation capability
-> typed result or refusal
-> EvidencePacket
-> EventRecord
-> read-only projection
```

Forbid:

```text
arbitrary shell commands
private tool calls
broad dispatch
provider/model calls
network calls
worker execution
Workbench apply behavior
preview/apply/rollback
repository mutation
branch/worktree automation
GitHub mutation
release or promotion
```

Stop at `needs_review` with `PASS_WITH_WARNINGS` and recommend exactly:

```text
AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```
