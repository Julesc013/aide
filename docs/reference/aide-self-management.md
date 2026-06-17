# AIDE Self-Management

## Purpose

AIDE must be able to manage AIDE as a repo.

This means AIDE manages its own structure, knowledge, docs, evidence, queues,
reports, schemas, policies, generated outputs, and migration safety using the
same discipline it offers to other repositories.

Machine-readable doctrine lives in `.aide/policies/self-management.yaml`.

## Doctrine

AIDE self-management is not automatic cleanup.

It is a reviewed loop:

```text
observe
-> classify
-> compare
-> explain
-> plan
-> dry-run
-> validate
-> review
-> apply only if authorized
-> record evidence
-> emit events
-> update OKF when authorized
-> reconcile again
```

The rule is:

```text
AIDE should never clean up itself by intuition.
AIDE should clean up itself by protocol.
```

## Self Profile

The proposed self-management profile is:

```yaml
id: AIDE_SELF_PROFILE
authority_mode: self_hosted
canonical_profile: .aide/profile.yaml
canonical_queue: .aide/queue
knowledge_bundle: .aide/knowledge/okf
runtime_state: .aide.local
mutation_mode: queue_gated
apply_mode: reviewed_transaction_only
```

This task does not mutate `.aide/profile.yaml`. The profile above is doctrine
for future review.

## Managed Surfaces

AIDE self-management covers:

- repository structure;
- root authority;
- OKF knowledge;
- documentation truth;
- queue health and review-gate debt;
- generated outputs;
- evidence lifecycle;
- protocol and schema lifecycle;
- tools and scripts;
- tests, fixtures, and evals;
- safety and secrets.

## Current Live Inputs

Current Track B evidence reports:

- repo layout inventory reports 5,136 files, 943 generated files, 2,687
  evidence files, and 608 orphan candidates;
- root status reports 22 roots, 3 mixed roots, 19 unknown or review-required
  roots, and 15 high-risk roots;
- `.aide/reports` has 102 top-level files, 52 directories, and 365 flat
  check/accept report path references across 156 files.

These facts are warning and planning evidence. They are not deletion,
movement, or rationalization approval.

## Object Backlog

Future self-management objects should start report-only:

- `RootAuthorityManifest`
- `RepoLayoutInventory`
- `FileAuthorityRecord`
- `GeneratedOutputRecord`
- `DocTruthFinding`
- `KnowledgeDriftFinding`
- `QueueHealthFinding`
- `ReviewGateDebtRecord`
- `StructureTransaction`
- `ReferenceRewritePlan`
- `PathAliasRecord`
- `MigrationLedgerEntry`
- `ArchiveFateRecord`

The first priority is `RootAuthorityManifest`, because it answers what belongs
where.

## Command Backlog

Future commands should also start report-only:

```text
aide structure status
aide structure inventory
aide structure authority
aide structure lint
aide structure explain <path>
aide structure plan
aide structure dry-run
aide structure validate

aide knowledge status
aide knowledge project
aide knowledge lint
aide knowledge explain <page>
aide knowledge affected --since <ref>

aide docs status
aide docs link-check
aide docs truth-check
aide docs stale-claims

aide queue health
aide queue debt
aide queue supersessions
aide queue next

aide generated status
aide generated explain <path>
aide generated refresh-plan
aide generated validate

aide evidence status
aide evidence index
aide evidence validate
aide evidence explain <id-or-path>

aide migrate map
aide migrate validate-map
aide migrate dry-run
aide migrate alias-plan
aide migrate reference-plan
```

## Non-Goals

Self-management does not mean:

- freely reorganizing the repo;
- deleting orphan candidates automatically;
- rewriting queue history;
- hand-editing generated OKF pages;
- trusting reports without evidence;
- applying broad migrations without review;
- treating docs as truth over queue, protocol, and evidence;
- hiding stale claims by regenerating everything.

## Initial Queue Sequence

The first sequence is:

1. `AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01`
2. `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`
3. `AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01`
4. `AIDE-BUILD-DOC-KNOWLEDGE-TRUTH-RECONCILER-01`
5. `AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`
6. `AIDE-BUILD-QUEUE-HEALTH-REPORT-01`
7. `AIDE-BUILD-STRUCTURE-FATE-MAP-01`
8. `AIDE-BUILD-FIRST-SAFE-STRUCTURE-TRANSACTION-01`

Each build task should be report-only first unless a later reviewed task
explicitly authorizes a tiny apply-capable transaction.
