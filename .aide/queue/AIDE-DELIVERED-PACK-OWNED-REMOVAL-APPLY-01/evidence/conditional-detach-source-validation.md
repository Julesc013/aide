# Conditional detach source candidate

Date: 2026-09-25. Branch/worktree:
`task/aide-lifecycle-removal-apply-01`,
`D:/Projects/AIDE/aide-lifecycle-removal-apply`.
Current HEAD at verification: `ed366600dbc18435da16ee6b1c29e729c53739a8`.
This is an uncommitted source candidate, not an integrated or release result.

## Behavior and boundary

The prior partial apply now recognizes an exact whole `AGENTS.md` scaffold
generated for a new project. It requires the receipt-managed section digest,
the complete observed file digest, and a same-handle Windows digest/delete
check. It removes the installed runner last. If every receipt-owned path is
removed or already absent, it deletes the exact receipt, then the removal
intent, and reports `DETACHED`. Empty directories, project-owned state and
unknown files remain. An interrupted run retains the intent. If the receipt
was retired before interruption, the extracted pack CLI can reconcile that
intent only when all recorded effects and previously absent paths remain
absent. A newly created file on such a path causes `RECOVERY_REQUIRED`.

An authored brownfield `AGENTS.md` is not edited. It and any changed or unknown
recorded material are preserved, along with the installed runner and receipt;
the result remains `PARTIAL_REMOVAL` with exit code 2. A safe anchored edit of
only the managed section inside authored content remains unimplemented.
Non-Windows apply still fails closed. This work does not implement general
rollback or deletion of target-owned material.

## Verification

- Ten adversarial removal tests passed in 145.116 s using the external runner
  `D:/Projects/AIDE/_review_scratch/removal-provisional-helper-tests.py` and
  frozen helper snapshot SHA-256
  `19172514cd0e5a50c9228e897412483f40c3dcf3d8e7c0b353726cde30c68f3a`.
  They cover brownfield preservation, fresh detach, interruption and resume,
  post-receipt reconciliation, already absent paths, a new file appearing at
  an already absent path, stale plan/receipt, changed AGENTS at effect time,
  changed leaf, parent junction, competing writer/delete handles and hard links.
  Log: `D:/Projects/AIDE/_review_scratch/removal-final-adversarial-tests.log`,
  SHA-256 `304b0105cb24f02ed4b3c47e6b81aa781083d2e85128260ca402deb51bb5b9ad`.
- Three existing removal-planner tests passed in 45.332 s without helper
  injection. Log SHA-256
  `fa49b661801a4a7efe919a6cb2c4f13bbdfe44f21e4bd20e91643c4f5f50496d`.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py
  .aide/scripts/tests/test_export_import.py`: PASS.
- `git diff --check`: PASS.
- Canonical `validate`: FAIL only at export-pack/pack-status provenance; its
  tracked pack manifest binds `1a25e33e` while this branch HEAD is `ed366600`
  with new source. Log SHA-256
  `bc59a9ec6f1256dd0e348f2ac26e5d9384618e5bb06cce323d8448b4d1b0bf5b`.
  Canonical `doctor`: FAIL as a consequence of validation failure. Log SHA-256
  `4ce8ead11ef9129070e488909f540a4d6c40ee51fbb9186b7af5d3b77f8f2b7f`.
  No generated outputs were refreshed in this isolated source branch.

## Exact files and dependencies

Source SHA-256 `0c120c8a28723846a9a4b7fa2cc0a9faf1f3064caad85190773664286f185629`.
Test SHA-256 `83043d4723d497adfcaed2183e43096e0b74eeafa6554673ab1c91148868b05c`.
Documentation SHA-256 `751ebebeb981659bf60514f1c1e18b7fcf2788c518d696a82e4950559574f396`.
The source refers to `portable_lifecycle_lock`,
`windows_pinned_directory`, and `atomic_create_bytes_no_clobber` from the
separate owned-repair implementation. Its direct runtime tests cannot pass on
this old branch alone. The provisional in-memory helper injection is an
interface check, not combined-source qualification. Root must merge accepted
helper ancestry, then run actual combined tests, generate and qualify delivered
artifacts, obtain independent review, and integrate only an accepted candidate.
