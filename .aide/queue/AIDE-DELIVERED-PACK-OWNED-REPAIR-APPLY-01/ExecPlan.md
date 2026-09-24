# ExecPlan: Owned-file repair apply

## Objective and scope

Add an explicit portable CLI repair for one missing managed file. The source must be the exact checksum-valid pack recorded in the target receipt. Only a missing target with matching managed-file receipt evidence may be restored. The old report-only repair model remains separate.

## Allowed paths and dependencies

The allowlist is in `task.yaml`. Depend on the existing delivered importer receipt, path safety, pack checksum, and atomic-write helpers. No shared generator or Git mutations are in scope.

## Plan

1. Characterize receipt and import intent behavior and add explicit repair command.
2. Bind dry-run and apply to exact plan digest; journal before writing; classify interrupted recovery.
3. Test successful extracted consumer restore, tampered pack/receipt, existing edit, stale plan, unsafe path, and interruption.
4. Record commands, results, and remaining gaps under `evidence/`; stop at review.

## Recovery and idempotence

An existing repair intent blocks new work. A completed postimage is finalized by removing the intent; a missing preimage can be retried only with its original plan identity. Unknown observed bytes remain blocked. Dry-run never changes target state.

## Progress

- [x] Inspect clean bounded worktree and existing contracts.
- [x] Implement and test.
- [x] Record evidence and request independent review.

## Decisions

Repair targets one missing managed file. Existing modified bytes, managed sections, target-owned templates, rollback, and removal are deferred to separately reviewed operations.

## Validation and retrospective

The extracted-pack CLI completed a missing-file restore in a disposable consumer. The full importer suite (32 tests) and a final focused four-test repair suite passed. `doctor`, `validate`, compilation, and diff whitespace checks passed. This candidate stops at independent review without Git or shared artifact generation. The validated extracted pack is matched through its manifest/checksums and receipt identity; signing or a published archive digest is outside this bounded repair operation.

Owner review identified a final-write race in the first candidate: `os.replace` could overwrite a file created after the missing-preimage check. The implementation now stages full bytes and publishes through no-clobber hard-link creation. A deterministic competing-creation regression and a prepublication-failure retry regression were added; the final focused six-test result is recorded in evidence. An abrupt process termination between staging and cleanup may leave an unreferenced temporary file; the target payload and intent remain classifiable, and automatic temp cleanup is deferred pending ownership-safe cleanup rules.
