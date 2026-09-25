# Removal source review repair candidate

Date: 2026-09-25. The independent review of commit
`d13894ba0f55b94daa46ce31714489d9228c9522` returned
`REQUEST_CHANGES`. Original review:
`D:/Projects/AIDE/_review_scratch/removal-d13894ba-independent-review.md`,
SHA-256 `a987f630747195eb423bfb5aa15d017bcda004ac019eb20ad7cf03678be834b0`.
This record describes uncommitted changes on
`task/aide-lifecycle-removal-apply-01` after that commit. It is a new review
subject, not acceptance of the rejected commit.

## Repairs

- A resumed managed-file removal intent now requires the preimage digest to
  equal the receipt's installed digest. Rehashing an intent with a later
  authored file's digest cannot authorize deletion.
- A resumed standalone `AGENTS.md` operation must still match the exact
  generated whole-file scaffold and receipt-managed block. A rehashed intent
  pointing to an authored file returns `RECOVERY_REQUIRED` before effects.
- A managed path already absent at planning is preserved in the receipt. The
  runner and receipt remain and status is `PARTIAL_REMOVAL`; absence alone
  cannot authorize terminal retirement. Older intents with a nonempty
  `settled_absent` list fail closed for manual reconciliation. This is a
  deliberate narrower completion rule.

## Tests and source identity

The temporary test runner
`D:/Projects/AIDE/_review_scratch/removal-provisional-helper-tests.py`
injected only the three missing shared primitives from frozen snapshot
SHA-256 `19172514cd0e5a50c9228e897412483f40c3dcf3d8e7c0b353726cde30c68f3a`.
It did not edit source or establish combined-source acceptance.

- Four affected/adversarial tests passed in 73.470 s. Log:
  `D:/Projects/AIDE/_review_scratch/removal-review-repair-focused.log`,
  SHA-256 `ff6edc09ce18a7fb5afe58efb8b38c912fa6144078305376e203dbfc52883ab9`.
- Twelve removal tests passed in 185.261 s. Log:
  `D:/Projects/AIDE/_review_scratch/removal-review-repair-full.log`,
  SHA-256 `45bc7bfc1d2bbdad3d6e0208fb070f7af1a9cb9cab8ddc623e9c7d746882b8e6`.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py
  .aide/scripts/tests/test_export_import.py`: PASS.
- `git diff --check`: PASS.

Source SHA-256
`4f470add4339c9ea6c2b6f804881a31319d4d4250a6ff3c68749ecdc0175f018`.
Test SHA-256
`0f724a0bd5d5fff56cf8fbf9556596fef60d911f7db0657d26da37bec5a8e2a4`.
ExecPlan SHA-256
`3566aa51e848a4b098105102918cda25717df18205661d010dcf7866c3daed16`.

## Retained gates and limitations

The authored brownfield `AGENTS.md` managed section remains unchanged and
keeps the receipt, so full removal is not yet implemented. Previously absent
paths also keep the receipt and runner. The candidate still depends on the
separate shared-helper integration; direct tests on this old branch cannot
exercise the combined source. Generated pack provenance in this branch is
stale, as recorded in `conditional-detach-source-validation.md`. No artifact
regeneration, consumer mutation, independent rereview, dev integration, or
release qualification was performed for this repair candidate.
