# Frozen artifact/effect review finding, 2026-09-25

- Exact reviewed candidate `22257dc6ad9e08d5b656895d251f20b38c7f1fb5`,
  tree `dd1f40bb466ac6c03d94679dca2183dda6eddda7`.
- Independent reviewer: Codex subagent `/root/customization_review`.
  Verdict **REQUEST_CHANGES; no dev GO**. External original retained at
  `D:/Projects/AIDE/_review_scratch/stable-lite-current-projection-20260925/independent-artifact-effect-review.md`,
  SHA-256 `917adf6b5f60342476dc877785577c1573959df77ca1103ed554fb8819eabdea`.
- Finding 1: prior WorkUnit evidence and frozen external effect manifest cited
  an 11-commit range check belonging to `10fd7a20`. The reviewed effect
  candidate `22257dc6` has 12 commits after `dev@d292253b`. Independently
  reviewed and controller-run exact 12-commit range checks passed; controller
  log `frozen-candidate-commit-range.log` SHA-256
  `b068e30f6e8e7f87fbc3683c7801fa8cfce1d3d0edaf1a0ae112b68fb869eb73`.
  A superseding evidence commit changes the count again, so the final exact
  range must be run after it is frozen and bound in a new external effect
  manifest. The original 11-commit result remains valid historical evidence
  for `10fd7a20` only.
- Finding 2: `status.yaml` still said committed replay remained open despite
  passing zero-change receipts at `10fd7a20` and `22257dc6`. Correct the
  status to distinguish completed replay from still-open review/dev effect.
- Positive independent checks remain bound to `22257dc6` only: ZIP/tar and
  833 safe matching members, 830 embedded checksums, seven release checksum
  entries, nine asset-index entries and 12 Q48 asset entries matched;
  bundled CLI matched clean source `0509e161`; draft/no-publish boundary,
  canary logs, canonical checks and exact 12-commit policy check passed.
  These results do not authorize a changed candidate automatically.

This corrective change is evidence/status only. It does not alter source,
pack, archive, release metadata or hosted/native effects. Request focused
independent rereview of the superseding exact candidate before any dev effect.
