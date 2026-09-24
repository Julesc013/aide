# Fresh exact historical-disposition mechanism review — 2026-09-24

Decision: **ACCEPT_WITH_NOTES for mechanism source integration only**.

Reviewer: current Codex primary agent (`/root`), executing as
`BLACKGLASS-WIN1\Jules`. This reviewer did not author the historical candidate.
The client thread identifier was unavailable. This is a fresh review, not the
earlier review at `154daeee` and not an owner decision on any disposition.

Subject: published commit `59b886db75a534615808c37a85e4fbe24c28eda1`,
tree `05728830f839839cd27fecc19421a922609a0a4d`, historical base
`c6fdc754844cf7d42302218ce08307a7e05dcb61`. The branch was clean before
and after review. Current remote dev `3bdeb220cb31dfc3177faa6836f5e86c8071d1ef`
was not the review base.

## Prior findings

- Replacement refs: range traversal, latest-message read, and exact Git object
  facts now disable replacement objects. The adversarial fixture confirms that
  a conforming replacement message cannot turn the original malformed commit
  into a raw pass.
- Accountable acceptance: an accepted record requires an exact structured JSON
  decision matching disposition id, commit, tree, message hash, scope, decision,
  allowlisted reviewer, and date within the policy window. A request alone,
  untrusted reviewer, or future date is refused in focused tests. A responsible
  human decision is still required outside this mechanism review.
- Whole registry: every entry is checked before a matching record can apply;
  malformed neighbors and duplicate ids fail closed in focused tests.
- Whitespace: `git diff --check c6fdc754..59b886db` passes.

## Reproduced checks

- `test_q27_commit_recovery.py`: 22 passed, zero failed.
- `test_q31_export_pack_governance.py`: 6 passed, zero failed.
- All three exact real records match their commit, tree, ordered parents,
  message hash, failed checks, and record digest; the registry has zero errors.
  Raw range checks exit 1 with respectively 1, 13, and 1 original failures.
  Default range checks exit 1 with `proposed` and ineffective for each.
- `commit check --range c6fdc754..HEAD --no-dispositions`: 10 of 10 branch
  commits pass. `pack-status`, canonical `validate` and `doctor`, and local
  release validate passed in the old branch checkout. General policy and schema
  are in the portable export; the source-specific registry is absent.
- The earlier task evidence records 25 portable consumer tests; those were not
  rerun in this review. No source file was edited here.

## Integration notes and limits

Running `release validate` followed by `release draft-validate` on the old
branch made two draft asset checksums stale; draft validation exited 1, and five
tracked generated release files changed. Their diff was retained externally as
`historical-59b886db-release-sequence.diff` (SHA-256
`5618e81834447faaf1a55847c10e5dcd0e2ec36f7377f714f68f16a4541ed01b`).
Those five generated files were restored, leaving the reviewed branch clean.
The current repaired release generator and outputs on dev must be preserved;
integrate only eligible mechanism source and regenerate current derived outputs
from the combined source. This review does not accept the old branch's release
snapshot as a final artifact.

The three real dispositions remain proposed. This verdict neither accepts nor
rejects them, and does not authorize main promotion, tags, upload, public
release, hosted effects, or native qualification.
