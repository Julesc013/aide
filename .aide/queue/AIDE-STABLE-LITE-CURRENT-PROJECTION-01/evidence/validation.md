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
- NOT RUN: clean zero-change replay, exact artifact/dev effect review, dev
  integration, main, tag, public release or downloaded-byte acceptance.
