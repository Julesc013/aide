# Findings Summary

## Result

`PASS_WITH_WARNINGS`

## Counts

- total: 12
- info: 3
- warning: 9
- error: 0
- blocker: 0

## Material Warning Findings

- `DKT-003`: self-management policy sequence still lists
  `AIDE-BUILD-ROOT-AUTHORITY-MANIFEST-01` before this reconciler, while the
  accepted charter acceptance routes this reconciler next.
- `DKT-004`: self-management reference doc still contains the earlier initial
  queue sequence.
- `DKT-005`: latest generated task packet is stale relative to accepted Track B
  routing.
- `DKT-006`: OKF next-work projection is stale.
- `DKT-007`: OKF queue current-state page still describes the older OKF build
  slice.
- `DKT-008`: selected OKF pages contain stale source hashes for
  `.aide/queue/index.yaml`.
- `DKT-009`: README still describes Reconciler reports as planned even though
  the minimal report-only Reconciler was accepted with warnings.
- `DKT-010`: DOCUMENTATION.md groups Reconciler and CapabilityManifest with
  future phases instead of distinguishing accepted, checked, and planned state.
- `DKT-011`: selected documentation/report path references do not resolve.

## Informational Alignment Findings

- `DKT-001`: accepted self-management charter routes to this build task.
- `DKT-002`: this build task is present in the queue index.
- `DKT-012`: selected acceptance/check status evidence refs resolve.

All findings recommend `AIDE-CHECK-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` as the
next task. No finding authorizes repair.
