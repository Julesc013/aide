# AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01

Create and process:

```text
AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

Use `.aide/queue/index.yaml` as canonical queue truth. Re-read live repository
state before writing anything. Repository artifacts outrank this prompt,
generated packets, prior chat, and stale planning notes.

This is the next milestone after accepting `dominium_readonly_seam_v0`.

Build a deterministic, offline, read-only WorkUnit validation slice:

```text
deterministic Dominium context fixture
-> ContextDescriptor
-> ContextPack v2
-> WorkUnit
-> registered Dominium validation command
-> typed result or refusal
-> EvidencePacket
-> EventRecord
-> read-only projection
```

Required boundaries:

```text
no model
no provider
no worker
no target mutation
no Workbench mutation
no preview/apply
no Dominium command invocation unless a future reviewed task explicitly changes the accepted boundary
```

Do not implement live runtime, Workbench integration, provider/model calls,
worker dispatch, PatchTransaction apply, branch/worktree automation, GitHub
mutation, release, or promotion.

Materialize the task packet, ExecPlan, prompt, status, evidence, reports, tests,
and validation records. Stop at `needs_review`.

Do not begin this task from the acceptance task.
