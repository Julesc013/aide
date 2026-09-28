# Removal rename-gap recovery qualification

- Source: `526dfb5191f3bacd9ad644a4d6b093c3d545eeab`, tree
  `32069c8dca49dd87f27932726fc56dff782692d6`, based on frozen
  `dev@2aaee82e96d275d83501785a073f6ba73c7b6594`.
- Earlier candidate `d3b2f0d3` received independent REQUEST_CHANGES for an
  uncaught missing-identity legacy intent; see
  `removal-rename-review-d3b2f0d3.md`. The superseding source guards that
  field before path or handle access.
- Managed D job `f82663ff5b5d4911813e73c1b65e7b08` exited 1: the new
  positive test expected the wrong `AGENTS.md` whitespace, although the
  actual removal returned `DETACHED`. The test oracle was corrected to the
  receipt-derived planner postimage.
- Managed D job `338933ad49a54dbc97037b7e3908bd30` passed the corrected
  positive rename-gap case (1 test). Job `626c422a3b1e490ea7009499e476437f`
  passed adjacent backup-cleanup and interruption cases (2 tests).
- Managed D job `ff5eeb9bb4e64e7089a7ed2835397c16` passed the
  missing-identity legacy case (1 test, exit 0); peak memory 212,676,608
  bytes, peak scratch 243 bytes. Its scratch was retired and its reservation
  released. Retained receipt and bounded logs are under the approved D
  retained root for that job ID.
- Independent reviewer `/root/stable_effect_review` scoped rereview of exact
  `526dfb51` / tree `32069c8d`: **ACCEPT for dev source integration**. The
  guard returns false for a legacy intent; the caller returns
  `RECOVERY_REQUIRED` and retains intent/receipt. The reviewer confirmed
  no source change beyond this guard in the superseding delta and a clean
  `git diff --check`.
- Limits: the new legacy test calls the helper directly; full legacy
  end-to-end flow and hostile concurrent writers were not qualified.
  This is source acceptance, not acceptance of frozen Lite 1.0.0 assets or
  its release effect. Inclusion in that release needs regeneration and an
  exact artifact/effect review.

## End-to-end legacy retry and runner correction

- Test-only commit `dfe7fdf9` extends the interrupted brownfield fixture:
  a digest-valid legacy removal intent without file identity returns
  `RECOVERY_REQUIRED` through `apply_portable_removal`, keeps authored bytes,
  backup and intent, then finishes exact removal after identity restoration.
- The first managed attempt `85fd0fe0b4c44ea99c64b2547046db95` stopped
  before its test assertion. Live scratch monitoring saw two hardlinks for
  one owned 356-byte temporary/final file. The job was quiescent; the exact
  duplicate temporary link was removed after identity/ownership checks,
  then AIDE recovery retired its scratch and released the reservation.
  Receipt SHA-256: `41703f6d3bfe27f730f25ceaef6713920afbaed38ff6978d47730e0193115e98`.
  Exit is unknown, not a passing test.
- Initial runner fix `785e2fae` passed two focused scanner cases, 28 runner
  cases and the end-to-end removal case. Independent
  `/root/stable_effect_review` returned **REQUEST_CHANGES** because the live
  exception accepted an outside hardlink without proving all names were in
  owned scratch. Those passes remain historical, not acceptance of that fix.
- Superseding runner source `d2b587eb33619823123fd38b7b7b46c9be4c8284`,
  tree `67c64c3d4bc226c7b185f31316a57b2884322825`, counts linked names
  by device and inode and requires the observed owned-name count to match
  each file's link count. A scratch link to a sibling file is refused;
  reparse refusal and strict quiescent collection remain.
- Exact-source managed D jobs passed: `54c89bf1a44341bf9b79dfe501f89f62`
  (3 focused tests; receipt SHA-256
  `33c92aac9cbaef9cde8134ce27eed3baa7cc9026b590c0cea99d15e6c448fe77`),
  `9c72a8de37a345729fa24cff758f21c4` (29 runner tests; receipt SHA-256
  `ebec18336856cb2e87ea64d12b87028e2cda3b4f2055b138145bf85b1e20629d`),
  and `1d038d66b6724f0f9219a34b1d81db8a` (1 public removal retry test in
  62.133s; receipt SHA-256
  `2dcdf5386ee68f1c64054264e173f571a19f0a25f7fdca9a435252f5f124e5f9`).
  All exited 0, retired scratch and released reservations. Peak memory was
  214,200,320 bytes and peak scratch 17,420,415 bytes in the removal job.
- Independent `/root/stable_effect_review` **ACCEPTS** exact `d2b587eb`
  for dev source integration. The live scan is sampled evidence, not an OS
  sandbox or atomic guarantee against a hostile writer changing links
  between observations. Frozen Lite 1.0.0 assets/effect remain separate.
