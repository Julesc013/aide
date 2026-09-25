# Committed preview qualification, 2026-09-25

- Clean metadata candidate `10fd7a207f1644c5966e688092e03387e5e553e8`,
  tree `a0888730d121ae88736ba5063f1b15b464e87f69`, descends from
  `dev@d292253b` through all three independently accepted source repairs.
- Four release replay commands exited 0 and changed zero tracked/untracked
  paths; external receipt SHA-256
  `1c06b93fa3958d0221f114f5baf5c4d4e468ffbefab9677658465f4b554e2766`.
  ZIP SHA-256
  `68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c`;
  tar.gz SHA-256
  `d0b424563ea7a85d207546b0e2b0d381641e046659846876adbddf96a954073b`.
- Committed `pack-status` returned `PASS_SOURCE_ANCESTOR`, release boundary
  PASS; canonical `validate` and `doctor` exited 0/PASS. All three left the
  worktree clean. External `committed-canonical-receipt.txt` SHA-256
  `50565ccfda46dd30258de51d2603029c079d542a4bfff9cdaa02309f9cc8379f`.
- At `10fd7a20`, `commit check --range dev..HEAD` passed all 11 commits
  after `dev@d292253b`, log SHA-256
  `f15f0449c6bc2dc00a6ca3b5dd8dafd082e6c592ffde49f8bdb53c36ea359c84`.
  This check does **not** cover later evidence-only commits. At frozen
  `22257dc6`, an exact 12-commit range check passed; log SHA-256
  `b068e30f6e8e7f87fbc3683c7801fa8cfce1d3d0edaf1a0ae112b68fb869eb73`.
  A superseding candidate needs a new exact post-commit range receipt.
- Exact local draft remains preview-only/no-publish and contains corrected
  lifecycle claims. The 25-command extracted ZIP/tar canary and four-command
  installed Task OS canary bind the unchanged archive/CLI hashes in
  `projection-0509e161.md`.

At this `10fd7a20` checkpoint, independent exact artifact and `dev` effect
review was pending. The later rejected and accepted exact reviews and observed
effect are in `review-finding-22257dc6.md`, `review-acceptance.md` and
`observed-dev-effect.md`. Final stable profile, main/tag/publication and
downloaded-asset acceptance remain parent-campaign obligations.
