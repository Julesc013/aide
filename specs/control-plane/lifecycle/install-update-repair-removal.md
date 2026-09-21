---
type: AIDE Engineering Specification
title: Install, update, repair, rollback and removal
description: Lifecycle operations are governed transactions, not broad copy or cleanup commands.
status: draft
generated:
  by: aide-spec-unifier/1.0
  at: '2026-09-20T09:23:15.374486Z'
sources:
- id: P04
  resource: urn:aide:source-package:b3f3d0d27109a986e537928523c9c34f31e3458986c7632e97abee06d85db64c
  title: AIDE-Spec-Overhaul-2026-09-20(3)(1).zip
- id: P06
  resource: urn:aide:source-package:83f9926500c47e3ee8384868c7d4046083e2a75bef0d667fb526c8476446d121
  title: AIDE-Spec-Overhaul-2026-09-20-R2(2)(1).zip
- id: P09
  resource: urn:aide:source-package:fe066ea7e776bdd6f53ae3dc03b90f0da4c97b981acfd345cfb5fc4be343029b
  title: AIDE-Spec-Overhaul-2026-09-20-r2(5)(1).zip
- id: P13
  resource: urn:aide:source-package:8002f9f6c5fb08c7df8646795fcaf555d7e6fb0b57e02938fc1dec1af12c3cdc
  title: AIDE-Spec-Overhaul-2026-09-20-v2(1).zip
- id: P16
  resource: urn:aide:source-package:635f61aafab254ead0014e09e34a41acf9150282af60afbee0460157301a03a9
  title: AIDE-Spec-Overhaul-Refresh-2026-09-20(1).zip
- id: P18
  resource: urn:aide:source-package:d61e3fe58a17ae0b729d36519b23ba123de87571c55fcf0128f06e34e7c26723
  title: AIDE-Spec-Overhaul-v2-2026-09-20(1)(1).zip
- id: P20
  resource: urn:aide:source-package:90f79366cb02f34d737950db6708c087db367e36e7ce5ff98f7d953c6a82fb96
  title: AIDE-Specification-Overhaul-2026-09-20(1).zip
x_aide:
  profile: aide.engineering-spec/0.1
  adoption: proposed
  behavioral_qualification: not_run
  owner: recorded lifecycle writer
  applicability: lifecycle apply profiles
  requirement_ids:
  - UR-UPDATE-01
  - UR-UPDATE-02
  - UR-UPDATE-03
  - UR-UPDATE-04
  - UR-UPDATE-05
  - UR-UPDATE-06
  - UR-UPDATE-07
  - UR-UPDATE-08
---

# Install, update, repair, rollback and removal

<!-- AIDE-DRAFT-IMPORT:BEGIN -->
> **Imported draft, not an adopted contract.** This chapter preserves earlier
> proposed design for review in the live specification tree. Existing adopted
> foundation contracts retain precedence. Its `UR-*` / `UC-*` identifiers remain
> source aliases, not newly admitted `AIDE-*` requirements or passing tests.
> See [import status and source identities](../draft-import.md).
<!-- AIDE-DRAFT-IMPORT:END -->

Lifecycle operations are governed transactions, not broad copy or cleanup commands.

## Scope and authority

This is a proposed design contract. It is not runtime activation, target mutation permission or a claim that every requirement is implemented. Existing queue, policy, schemas, source and qualification records retain their owners.

## Design

An immutable UpdatePlan compares the last installed baseline, current target bytes and incoming component. Classify conflicts, exact writes, preserved regions, migrations, dependencies, target-native validation and rollback or forward-repair limits. Separate discovery/acquisition from effectful application. Review binds the exact plan and actual observed target.

Apply rechecks current identity, ownership and preimages, writes only the authorized set, verifies postconditions and records a receipt. Side-by-side generations and atomic activation are preferred where the platform proves them, but a rename is not a multi-file distributed transaction. Crash recovery must classify completed, no-effect, partial and unknown steps. A target that changed after upgrade may require a merge or forward repair rather than blindly restoring old preimages.

Detach and uninstall differ: detach may remove management while preserving useful project artifacts; uninstall removes only proven owned content according to retention. Package-manager and host-extension-manager ownership must be honored. Universal Setup may implement generic lifecycle mechanics where selected, but the AIDE component manifest and target project keep their own semantics and acceptance. No lifecycle command grants publication or protected-branch mutation merely because it can write files.

## Interface and data boundary

Distribution/installed/current identities; ownership ledger; semantic three-way plan; exact operations; protected regions; migrations; validation; receipts; rollback/retention; writer.

Reuse existing protocol owners before creating a new public kind. Wire objects, internal values, semantic validation, policy evaluation, fixtures and renderings remain separate. New fields below are design requirements, not an automatic wire-schema amendment.

## Proposed normative requirements

### UR-UPDATE-01 — Exact reviewed plan

Lifecycle apply MUST execute only an exact admitted plan bound to current target identity and preimages.

### UR-UPDATE-02 — Three-way reconciliation

Upgrade MUST compare previous installed baseline, current target and new package, preserving local changes or surfacing conflicts.

### UR-UPDATE-03 — Ownership-aware repair

Repair MUST restore the admitted installation contract without secretly adding features, weakening policy or deleting unrelated content.

### UR-UPDATE-04 — Recovery classification

Interrupted multi-file lifecycle changes MUST record per-step effects and qualify rollback/forward-repair rather than assume atomicity.

### UR-UPDATE-05 — Safe rollback

Rollback MUST detect user changes after the original operation and preserve or explicitly reconcile them.

### UR-UPDATE-06 — Preservation-first removal

Uninstall/detach MUST remove only proven owned material and obey declared evidence, user-data and project preservation rules.

### UR-UPDATE-07 — One lifecycle writer

Each installed resource MUST have one recorded lifecycle authority, including native package managers or selected Setup providers.

### UR-UPDATE-08 — Lifecycle qualification

Install/update/repair/remove claims MUST be tested in extracted installed consumer environments, including failure and offline cases.

## Acceptance design

The linked cases are **not run**. Each requires a pinned subject and environment, observed effects and an independently defined oracle. Package-local JSON or Markdown validation does not execute these scenarios.

| Case | Adversarial stimulus | Required observation |
|---|---|---|
| `UC-UPDATE-01` | New files appear after plan approval. | Scope does not silently expand to include them. |
| `UC-UPDATE-02` | The project edits a vendor-managed section. | Upgrade does not silently overwrite the local edit. |
| `UC-UPDATE-03` | Repair encounters a newer unapproved feature. | It remains excluded from the repair plan. |
| `UC-UPDATE-04` | Crash after some files are replaced. | Recovery knows the exact partial state and does not blindly rerun the whole update. |
| `UC-UPDATE-05` | The user edits a file after upgrade. | Rollback refuses stale restore or presents a conflict-aware plan. |
| `UC-UPDATE-06` | Unknown content exists under an install root. | It is retained or separately reviewed rather than recursively deleted. |
| `UC-UPDATE-07` | Both a package manager and AIDE updater claim a binary. | The conflict is resolved before either writes. |
| `UC-UPDATE-08` | Only source-checkout tests pass. | The package is not declared lifecycle-qualified. |

The proposed requirements and acceptance designs are retained inline above. The original bulk registers remain external review inputs; see [import status and source identities](../draft-import.md).

## Delivery boundary

Implement this contract only through a source-bound, queue-admitted vertical slice with existing consumers or a contrasting fixture. Separate source presence, local test results, operational qualification, activation and release support in the closeout record. Optional profiles do not become prerequisites for smaller supported profiles.
