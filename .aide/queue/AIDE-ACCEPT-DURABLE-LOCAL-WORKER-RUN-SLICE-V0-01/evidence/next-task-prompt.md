# AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01

Create and process `AIDE-PLAN-DISTRIBUTION-UPDATE-PROTOCOL-V1-01`.

Repo truth outranks attached handoffs, generated packets, prior chat, and stale
planning notes.

This is a bounded planning/oracle task for AIDE Lite distribution and update
protocol v1. It must not implement install, update, rollback, release
publication, target-repository mutation, GitHub release creation, package
upload, branch/worktree automation, provider/model calls, network calls,
Workbench runtime, MCP runtime, preview/apply/rollback, or promotion.

Use the 25 June 2026 portfolio/distribution handoffs as advisory input only.
Reconcile them with live `.aide/queue/`, `.aide/profile.yaml`, `PLANS.md`,
`IMPLEMENT.md`, and existing install/repair/upgrade/rollback/release boundary
records.

Produce a bounded executable plan for:

```text
DistributionManifest
ProjectLock
InstallRecord
OwnershipLedger
UpdatePlan
UpdateReceipt
RollbackBundle
AIDE self-consumer fixture
```

The plan must preserve:

```text
unknown ownership blocks automatic apply
install does not imply trust
conformance does not imply authorization
updates are planned, dry-run, evidenced, and review-gated before apply
AIDE source repository is not treated as an installed target
```

Stop at `needs_review` and recommend exactly the next build task needed to
materialize the first distribution/update protocol object.
