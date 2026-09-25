# Exact predecessor rollback source validation

Date: 2026-09-25. Source worktree:
`D:/Projects/AIDE/aide-lifecycle-rollback-apply`, branch
`task/aide-lifecycle-rollback-apply-01`, starting dev `b05ba7d5`.
This is an uncommitted source candidate awaiting independent review and
combined artifact qualification. No real target, shared ref, generator output
or remote was changed.

## Behavior

`rollback-pack` previews or applies a return from a completed safe-mode
portable update to the receipt's exact predecessor pack on Windows. Both
packs pass checksum validation; their manifest payloads equal their actual
files and have the same safe target set. The receipt binds both exact pack
identities and every managed baseline to the current pack source. The target
must still contain those installed managed bytes or managed `AGENTS.md`
block. Target-owned templates cannot be created or changed by this rollback.
Apply requires the exact preview digest and runs through the existing pinned
import transaction under the per-target lifecycle lock. Its effect-time
checks and target-local intent preserve uncertain interruptions.

## Verification

- Before implementation, the disposable v1 import → v2 update → v1 rollback
  test failed because `build_portable_rollback_plan` did not exist (one test,
  28.539 s, exit 1). This was the characterized regression.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p
  test_export_import.py -k rollback`: **PASS**, five tests in 182.503 s.
  The tests cover restored managed bytes and receipt via the installed CLI,
  preservation of project-authored bytes, stale preview, later edit, forged
  receipt baseline, wrong same-path predecessor, changed safe payload set,
  interrupted rollback and pending prior import intent. Log:
  `D:/Projects/AIDE/_review_scratch/rollback-source-frozen-tests.log`,
  SHA-256 `bb5010b61744ef00e685a939cadb6d8c7b99c7a4e0e6603de0246ab27dd5c2a5`.
- Two existing importer regressions for interrupted update and changed target
  after preview: **PASS**, 51.440 s. Log:
  `D:/Projects/AIDE/_review_scratch/rollback-import-regressions.log`,
  SHA-256 `7aa9884122b6615abcb62b47bfd6ed91ba73965436ad748a733a601ea5523e13`.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py
  .aide/scripts/tests/test_export_import.py`: **PASS**.
- `git diff --check`: **PASS**.
- `py -3 -B .aide/scripts/aide_lite.py validate`: **PASS**, log
  `D:/Projects/AIDE/_review_scratch/rollback-canonical-validate.log`,
  SHA-256 `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789`.

SHA-256 source `.aide/scripts/aide_lite.py`:
`9f979345f6be256186fce6d73067c98e7ef1813465898fcad3af9a34519829db`.
SHA-256 test `.aide/scripts/tests/test_export_import.py`:
`0451028bfa4f35ec85f0a80dcbb18c9f2a77fef1356f7af01b28a4c0da4e30cf`.
SHA-256 reference documentation:
`94136d753fe86df98f17224e2d55d805c8b625d14080e7768bffc386721c2c78`.

## Limits and next gate

This source cannot roll back without the exact validated predecessor pack,
or when safe payload paths changed between packs. It does not undo arbitrary
project-authored edits or reconcile mixed/unknown interrupted effects; those
retain `RECOVERY_REQUIRED` and require the import recovery path. It does not
claim POSIX apply, broad version migration, rollback of target-owned templates,
or full mandatory lifecycle coverage. Extracted final ZIP/tar consumers,
combined-source validation, independent technical review and dev integration
are still pending.
