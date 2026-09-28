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
