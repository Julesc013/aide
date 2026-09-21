---
type: AIDE Engineering Specification
title: Workspace estate, storage and retirement
description: A workspace is a governed execution resource, not just a folder or Git worktree.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P11
  resource: urn:aide:source-package:829c23fed34643bc083f60c1fe78ef995ede4b5188f5799e2165b01be9ca78d6
  title: AIDE-Spec-Overhaul-2026-09-20-R2(7)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: workspace/storage owner
  applicability: workspace-managed profiles
  requirement_ids:
  - UR-ESTATE-01
  - UR-ESTATE-02
  - UR-ESTATE-03
  - UR-ESTATE-04
  - UR-ESTATE-05
  - UR-ESTATE-06
---

# Workspace estate, storage and retirement

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

A workspace is a governed execution resource, not just a folder or Git worktree.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

Separate repositories/object stores, checkouts, workspaces, build roots, scratch, caches, evidence stores and quarantine. Each has an identity, owner, storage profile, capacity, sensitivity and lifecycle. Resolve actual volume properties rather than infer them from a path. A linked worktree shares Git authority and is not a complete security boundary.

Use toolchain-native filesystems for mutable builds when required. Cross-OS shares, sync folders and removable media may be transport or source locations without being safe database/build locations. Supply leased temporary roots and cache variables to AIDE-launched processes without globally rewriting the user environment. Capacity reservations and hard quotas must be distinguished.

Retirement checks active processes, leases, unresolved effects, unique commits, untracked content, open review, artifact reachability and retention. Age or branch-merge ancestry alone is insufficient. Preserve a recovery capsule for valuable dirty/unique state when permitted, test its restoration and secret-scan it before wider sharing. Quarantine or grace periods should precede destructive cleanup where appropriate. A tombstone records what was removed without retaining private content forever.

## Interface and data boundary

Pool/volume identity; filesystem capabilities; workspace/base/owner; lease/fence; mounts; quotas; build/scratch roots; retained artifacts; unique work; retirement/restore receipt.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-ESTATE-01 — Workspace identity

Workspaces, Git object stores, checkouts and build roots MUST be distinct resources with explicit ownership.

### UR-ESTATE-02 — Storage qualification

Placement MUST consider actual filesystem, permission, case, link, locking, locality and capacity properties.

### UR-ESTATE-03 — Capacity reservations

Workspace/scratch/cache allocation MUST use bounded reservations and disclose hard versus monitored limits.

### UR-ESTATE-04 — Retirement reachability

Retirement MUST inspect active work, effects, unique content, references, release/support holds and ownership before deletion.

### UR-ESTATE-05 — Recoverable valuable state

Destructive retirement of valuable dirty/unique state MUST retain an authorized restoration-tested recovery record or explicit disposal decision.

### UR-ESTATE-06 — Contained scratch

AIDE-launched tools MUST receive scoped temporary/output roots without silently changing global user configuration.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-ESTATE-01` | Create a linked worktree for an untrusted worker. | The system does not claim independent Git or credential isolation. |
| `UC-ESTATE-02` | A toolchain is moved to an unsafe shared build tree. | Placement refuses or selects a qualified staging location. |
| `UC-ESTATE-03` | Parallel jobs request more disk than the pool allows. | New allocation is blocked before unbounded writes. |
| `UC-ESTATE-04` | A stale workspace contains an unpushed fix. | It is not deleted merely by age. |
| `UC-ESTATE-05` | Cleanup would remove a failed experiment with useful artifacts. | Its value is harvested or preservation is explicitly decided before removal. |
| `UC-ESTATE-06` | A build needs TMPDIR and cache variables. | They are injected only into the admitted process environment. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
