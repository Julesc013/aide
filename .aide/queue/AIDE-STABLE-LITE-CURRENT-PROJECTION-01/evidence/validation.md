# Validation, 2026-09-25

- PASS: six serial current-generator commands, exact logs and hashes in
  `projection-0509e161.md` and the external generation receipt.
- PASS: clean-source release/export provenance, local preview/no-publish
  draft wording, ZIP/tar checksums and 833 equal safe archive members.
- PASS: pre-commit `pack-status`, canonical `validate`, `doctor`, 18 Q47,
  12 Q48 and 11 Task OS source tests.
- PASS: 25-command extracted ZIP/tar fresh/brownfield consumer and four
  extracted-CLI empty/one-item target Task OS checks.
- FAIL, retained: initial Task OS canary oracle wrongly equated latest
  packet ID with latest indexed queue ID. Corrected external oracle and
  replay passed; no product source change followed from that failure.
- PASS: `git diff --check` before projection staging.
- FAIL, retained: first post-commit four-command replay changed 18 release
  metadata files while leaving ZIP/tar bytes unchanged. A bounded metadata
  convergence and clean replay are required.
- PASS: clean second four-command replay on committed `10fd7a20` changed
  zero tracked/untracked paths and preserved ZIP/tar hashes. Committed
  pack-status, validate, doctor and its exact 11-commit policy range passed.
- PASS: evidence-only `22257dc6` also had zero-change replay and its exact
  12-commit range check passed. Superseding evidence needs a new final range.
- REQUEST_CHANGES: independent exact `22257dc6` artifact/effect review found
  stale 11-commit citation and contradictory replay-open status. No dev GO;
  the report and hash are in `review-finding-22257dc6.md`.
- PASS_WITH_NOTES: focused exact `6e8af2bd` artifact/effect rereview accepted
  the corrected record and permitted only local dev FF plus normal push.
- PASS: fresh Windows/GitHub identity, four base refs, ancestry, clean
  worktrees, checked locks and archive hashes; local FF, push and four
  post-effect ref reads matched `6e8af2bd` and tree `a964b2e2`.
- PASS: supplemental 31-command Windows lifecycle local preview canary on
  the same ZIP; all 31 command-log hashes/exits matched on audit.
- NOT RUN: main promotion, tag, public release or downloaded-byte acceptance.
