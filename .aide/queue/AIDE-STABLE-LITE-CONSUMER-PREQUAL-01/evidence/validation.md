# Validation, 2026-09-25

- PASS: exact local ZIP SHA-256
  `8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`;
  the prior extracted ZIP/tar 25-command update/customization canary remains
  bound to the predecessor release projection WorkUnit.
- PASS: clean extracted-ZIP safe import into a new target, exact-plan apply,
  installed `context` and `pack --task` exit 0. Installed `verify` exits 0
  with zero errors and 15 classified warnings. See
  `evidence/admission-and-context-probe.md` for exact run paths and log hashes.
- PASS WITH NOTES: the second external lifecycle canary exits 0 with 31
  delivered CLI commands. Controller independently checked all 31 command log
  hashes and exit codes, with zero mismatches. Independent exact-script/result
  reviewer issued `ACCEPT_WITH_NOTES`, report SHA-256
  `ddb9dbf66ff59885279ee6f0ef2595019ff84ae04830edbb8f35a67018c30b71`.
  The first attempt's harness timeout remains failed and separate. See
  `evidence/lifecycle-local-preview.md` for the exact subject and notes.
- FINDING: from the clean installed target, `task status` exits 1 with
  `task_count: 0` but reports `latest_task_id: Q17` and recommends `X-OS-01`.
  Log SHA-256
  `d2bb16e19fd66b8437a88d2f454841f71e2dc04162d53ac1fe2ebb9c7882e81e`.
  The empty-queue exit 1 is source-defined; the misleading task identity and
  next-work suggestion require bounded source repair and delivered recheck.
- PASS: `py -3 -B .aide/scripts/aide_lite.py task inspect --task-id
  AIDE-STABLE-LITE-CONSUMER-PREQUAL-01` reports `needs_review`,
  `classification: complete`, zero missing evidence. `workunit validate`
  exits 0/PASS for 380 source queue tasks and reports no queue mutation;
  its four generated report outputs were restored from this task worktree
  after reading the result, leaving only allowed queue/docs changes.
- PASS: `git diff --check` reports no whitespace errors before staging.
- NOT RUN: final downloaded-byte consumer, real published version pair,
  OS-level offline trace, forced process kill, native/hosted or restricted
  principal qualification. These remain release/profile gates.
