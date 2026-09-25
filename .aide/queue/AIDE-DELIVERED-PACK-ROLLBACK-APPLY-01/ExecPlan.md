# ExecPlan: exact predecessor portable rollback apply

## Objective and scope

Provide a real Windows delivered-pack rollback from a completed safe-mode
update to its exact validated predecessor pack when both packs have the same
safe payload targets. Preserve project-owned and unknown material. Use the
existing importer transaction, pinned Windows effects, receipt and recovery
intent; add a narrow rollback gate and exact preview binding.

Allowed paths are source, its export/import tests, one reference document and
this WorkUnit. No shared generated artifacts, real targets, Git refs or
publication are in scope.

## Dependencies and observed limits

Completed import updates delete transient preimage backups. Therefore the
target alone cannot restore arbitrary prior bytes. The validated predecessor
pack must provide them, and the current receipt must bind that exact pack as
its predecessor. Added or removed payload paths need separately reviewed
ownership-aware handling and are excluded from this first apply slice.

## Sequence and verification

1. Add a disposable failing regression for v1 import, v2 update, exact-plan
   rollback to v1, and receipt identity. Characterize the failure.
2. Add stale-plan, authored-edit, wrong-pack, path-set, and interruption cases.
3. Implement preview/apply gates over the existing import transaction. Bind
   both pack identities, receipt lineage, safe mode and exact operation set.
4. Run affected tests and structural checks; record source hashes, commands,
   outcomes, unresolved cases and independent-review requirement.

## Progress

- [x] Inspected clean task worktree and existing importer receipt/recovery model.
- [x] Identified missing durable preimage backup as the exact full-rollback
  prerequisite; selected validated equal-payload predecessor scope.
- [x] Disposable v1→v2→v1 regression failed with missing
  `build_portable_rollback_plan` before implementation.
- [x] Added `rollback-pack` preview/apply and exact receipt, pack, payload
  and effect-time gates. Five focused rollback tests, two existing importer
  regressions, Python compilation, diff check and canonical `validate` pass.
- [ ] Independent review and combined artifact qualification.

## Independent review repair

Exact source `23422130` received REQUEST_CHANGES: its safe-pack enumerator
checked descendant reparse paths but not the `pack/files` payload root. A
checksum-valid Windows junction at that root escaped the declared pack while
passing enumeration. Retain the review and fixture; add a focused failing
regression for payload-root and pack-root junctions, reject those roots and
reparse metadata leaves before checksum reads, rerun affected tests, then
freeze a superseding source for exact delta rereview. Do not regenerate release
outputs or touch shared refs until that technical gate passes. The new
regression failed 1/1 before the guard and passed afterward; all six rollback
tests then passed. A fresh independent delta review remains pending.

## Current source checkpoint

The first source candidate was committed as `23422130` by the integration
controller and is rejected pending the reparse-boundary repair.
Changed paths are `.aide/scripts/aide_lite.py`,
`.aide/scripts/tests/test_export_import.py`,
`docs/reference/cross-repo-pack-export-import.md`, and this new WorkUnit.
`evidence/source-validation.md` holds exact file and log hashes. Do not
regenerate pack/release outputs or claim dev integration from this checkpoint.

## Recovery

A pending import intent is never reinterpreted as a fresh rollback. Its exact
effect state must be reconciled through the existing importer recovery path;
mixed or unknown effects remain `RECOVERY_REQUIRED`. Never infer ownership
from matching path names alone.
