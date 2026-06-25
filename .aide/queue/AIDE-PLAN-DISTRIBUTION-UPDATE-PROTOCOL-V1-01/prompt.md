# Prompt

Create and process `AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01`.

Repo truth outranks attached handoffs, generated packets, prior chat, and stale
planning notes.

This is a bounded planning/oracle task for AIDE Lite distribution and update
protocol v1. It must not implement install, update, repair, rollback,
uninstall, release publication, package upload, target-repository mutation,
Git tag creation, GitHub Release creation, branch/worktree automation,
provider/model calls, network calls, Workbench runtime, MCP runtime,
preview/apply/rollback, or promotion.

Use the 25 June 2026 portfolio/distribution direction as advisory input only.
Reconcile it with live `.aide/queue/`, `.aide/profile.yaml`, `PLANS.md`,
`IMPLEMENT.md`, and the existing Q43-Q48 lifecycle/release foundations.

Inventory:

```text
existing install planning schemas
existing ownership classifications
existing repair model
existing upgrade plan
existing rollback/uninstall model
existing export pack
existing release bundle
existing release-draft artifacts
existing golden tasks
existing managed-section behavior
```

Produce:

```text
distribution object dependency graph
v0/Q43-Q48 to v1 compatibility map
authority/source-of-truth map
ownership taxonomy
install/update lifecycle state machines
migration rules
refusal-code registry
artifact/source/channel model
rollout-ring model
fixture and conformance matrix
security and preservation invariants
public release gates
exact first build task
```

Freeze:

```text
Unknown ownership blocks automatic apply.
Install does not imply admission.
Conformance does not imply authorization.
An approved plan cannot expand its scope during apply.
Project-owned data is never silently overwritten or deleted.
Managed sections are modified only through exact managed-section identity.
Source-generated AIDE state is not copied into a target as target truth.
Every update has a preimage, postimage, evidence, and rollback path.
The AIDE source repository is never treated as the installed-target fixture.
```

Stop at `needs_review` and recommend exactly:

```text
AIDE-BUILD-DISTRIBUTION-MANIFEST-V1-01
```
