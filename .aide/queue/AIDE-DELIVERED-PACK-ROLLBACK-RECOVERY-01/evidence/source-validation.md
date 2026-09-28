# Exact partial rollback continuation source

- Base: `dev@76e17a4c2101a9f75fa1116b9256d331bd2cedb8`. One existing
  physical checkout; no release output, target repository or shared ref was
  changed. The final source commit/tree and independent verdict remain open.
- Behavior: rollback preview reports the saved import recovery digest only
  for an exact safe-mode rollback-direction intent. `rollback-pack
  --recover-partial --expect-plan <recovery-plan-digest>` invokes the existing
  guarded importer under the lifecycle lock. Ordinary rollback remains a
  refusal during a partial intent. Wrong direction, digest and rival target
  bytes refuse without retiring the saved intent or prior receipt.
- Regression before implementation: D-managed job
  `9d7d6075b2cc4f21a76e54623802c23f` failed one test at the absent
  `recovery_plan_digest` field; exit 1. The job was quiescent, retired scratch
  and released its reservation.
- First implementation run `12d5eb88345b441ebe922633c1e16f17` failed
  because the test addressed the frozen pack CLI without its `files/` prefix.
  This was a test path correction, not a product failure; scratch retired and
  reservation released.
- Focused corrected run `a666c6fa817c40dd8ede75b694602252`: **1 passed**
  in 85.664 seconds; exit 0, peak Job memory 263,659,520 bytes and scratch
  17,477,678 bytes. Exact CLI recovery returned `ROLLED_BACK_RECOVERED` with
  the predecessor receipt and authored README preserved.
- Affected rollback matrix `20f12d8a63a14f95ad758477650b502d`:
  **8 passed**, no skips, in 644.923 seconds; exit 0, peak Job memory
  262,639,616 bytes and scratch 24,886,835 bytes. It covered current
  rollback success, conflicts, path/lineage refusal, pending update/removal,
  interrupted recovery and pack reparse refusal.
- Additional CLI junction probe `ca2eb9c83e214eb68a87467228dfb3d4`:
  **1 passed** in 0.589 seconds, exit 0. It confirmed the existing CLI
  rejects a pack-root junction before using a checksum-valid alias.
- Every listed job used the shared finite D runner, ended quiescent, retired
  disposable scratch and released its reservation. Source tests are not a
  delivered-archive qualification. Completed/no-effect interruption states
  still use the existing importer reconciliation path; this new option is
  deliberately limited to an exact partial rollback.

## First review and repair

- Independent reviewer `/root/stable_effect_review` returned REQUEST_CHANGES
  for source commit `0bc7da3f` (tree `15c15d80`): pending rollback recovery
  bypassed the ordinary receipt lineage and equal safe payload path-set
  predicates. This is a substantive source finding, not an acceptance.
- The added reverse-import regression failed before repair in managed job
  `a0da9f7b315d41e19bd855b26084c665` (one expected failure, exit 1),
  confirming that differing payload paths reached the rollback recovery
  preview. Scratch retired and the reservation was released.
- A shared receipt-baseline predicate now precedes rollback recovery preview
  and ordinary rollback target observation. The exact regression passed in
  managed job `333950e2feef42e39a5ff04906561da5` (one test, exit 0),
  asserting refusal without changing the pending intent, prior receipt or
  partial target bytes. Scratch retired and the reservation was released.
- The superseding commit, affected regression result and independent rereview
  remain to be recorded. This source is outside the frozen Lite 1.0.0 assets.

## Superseding exact result

- Superseding source commit `72d1438e91f2294bb04c0fa6a0acaf924b35ba82`,
  tree `31b134b171d70c032bbec98c277f8d278a9bdc28`, passed the
  structured commit check. Its exact code and test hashes were used by
  managed job `22f2d9838c874d97bec66573caea94b6`.
- Affected rollback matrix: **8 passed**, no skips, 782.001 seconds, exit 0.
  Peak job memory was 263,368,704 bytes; peak scratch 22,190,909 bytes.
  Scratch was retired and reservation released. Full receipt is retained
  under the configured D: execution retained root.
- Fresh independent review of that exact commit/tree returned **ACCEPT for
  dev source integration**. See `source-review-72d1438e.md`. The earlier
  REQUEST_CHANGES remains part of history; this verdict supersedes it only
  for the repaired source.
- Source remains on its task branch to preserve the separate frozen Lite
  1.0.0 release subject. New delivered bytes and consumer qualification are
  required before claiming this behavior in a release.
