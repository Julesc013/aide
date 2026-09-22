# Historical Commit-Message Dispositions Independent Review

Date: 2026-09-22

## Decision

**REQUEST_CHANGES** for mechanism integration.

This review does not accept or reject any disposition. The three proposed
records remain proposed and ineffective.

## Reviewed Subject

- Branch: `task/aide-historical-commit-dispositions-01`
- Base: `c6fdc754844cf7d42302218ce08307a7e05dcb61`
- Head: `dea2cf7f4526c4874e1b3960b65d85f059836226`
- Head tree: `11f6586275e6e19201092ccbbddce3340404e641`
- Range: `c6fdc754844cf7d42302218ce08307a7e05dcb61..dea2cf7f4526c4874e1b3960b65d85f059836226`
- Commits in range: 7
- Worktree before review: clean and tracking the exact remote branch head

## Findings

### HIGH - replacement refs can turn a malformed commit into a raw PASS

`git_commit_messages_for_range` invokes ordinary `git log` at
`.aide/scripts/aide_lite.py:4520-4521`. It does not disable replacement
objects. Only the later tree/parent lookup sets `GIT_NO_REPLACE_OBJECTS=1` at
line 4558. A replacement therefore controls the message and traversal used by
the checker before exact-object disposition evaluation is reached.

A disposable-repository adversarial test created a malformed commit, created a
second commit object with the same tree and parent but a conforming message,
and installed a local replace ref. Before replacement, the malformed commit
returned `FAIL`. After replacement, the same requested full object id was
reported with the replacement message and `commit check --range <id>^!
--no-dispositions` returned exit 0 and `PASS`. The original tree lookup still
returned the original tree, which shows that the existing partial defense does
not protect raw message validation.

This contradicts `replacement_objects_disabled: true` and allows a malformed
historical commit to bypass both raw and disposition-aware range checks without
any disposition record.

Required fix: disable replacement objects for revision expansion, traversal,
and message loading, not only for the later fact lookup. Add a disposable test
that installs a replace ref and proves both default and `--no-dispositions`
checks still inspect the original commit message and fail.

### HIGH - accepted status does not prove an accountable decision

The accepted-record checks at `.aide/scripts/aide_lite.py:4734-4742` validate
only an `owner:`/`reviewer:` string shape and a parseable date. They do not bind
the identity to an authorized reviewer, reject a future date, or verify that
`decision_ref` records an acceptance of the exact subject. The current
`decision_ref` is a request that explicitly says silence and broad campaign
authorization are not decisions.

An in-memory adversarial evaluation changed each proposal to `accepted`, set
`reviewed_by` to `owner:untrusted-arbitrary-string`, set `reviewed_at` to
`9999-12-31`, and recomputed the self-digest. All three records became
`effective=True` with no errors while continuing to hash the unchanged
decision-request and raw-failure files.

The record digest and evidence hashes protect internal consistency, but they
do not authenticate authority or prove that an acceptance occurred. This does
not satisfy `accepted_human_review_required: true` or the prohibition on
self-approval.

Required fix: bind acceptance to a structured exact decision artifact that
states the disposition id, commit, decision, accountable identity, and review
date; require those fields to match the registry; validate the identity against
the reviewed authority set; and reject dates outside the allowed decision
window. Retain the request separately from the resulting decision.

### MEDIUM - invalid unrelated records do not fail the registry closed

`evaluate_historical_commit_disposition` selects records for only the current
commit at `.aide/scripts/aide_lite.py:4671` and validates only that match.
Malformed non-matching objects, non-object entries, and duplicate
`disposition_id` values on another commit are ignored.

Adversarial evaluations added each of those defects beside an otherwise
accepted exact record. In every case the matched record remained
`effective=True` with no errors. Duplicate records for the same commit are
correctly rejected, and wildcard/prefix records cannot match a full commit id,
but the registry as a whole is not validated as the policy and documentation
claim.

Required fix: validate every registry entry before any disposition can become
effective, enforce unique full commit ids and unique disposition ids, reject
non-object or schema-invalid entries, and add mixed-validity registry tests.

### LOW - the exact task range does not pass `git diff --check`

`git diff --check
c6fdc754844cf7d42302218ce08307a7e05dcb61..dea2cf7f4526c4874e1b3960b65d85f059836226`
returns exit 1 for a new blank line at EOF in `evidence/baseline.md` and
`prompt.md`. The validation record says `git diff --check` passed but does not
name the checked range, so it does not support the full-range claim requested
for this review.

Required fix: remove the two whitespace errors and record the exact range used
for the final diff check.

## Exact Proposal Verification

The three proposal records are truthful about the current formatter failures
and are ineffective:

| Commit | Tree/parents | Message hash | Failed checks | Evidence hashes | Record digest | Current effect |
| --- | --- | --- | --- | --- | --- | --- |
| `bfb86c12b9e6d2970024d29c57ba629994ec43cc` | match | match | exact 1 | match | match | proposed; false |
| `486e81cd3a918729f28e4b452a9dcff017238a04` | match | match | exact 13 | match | match | proposed; false |
| `1011d008fc39b135a5ef27062b5b8ee9c95cdc7f` | match | match | exact 1 | match | match | proposed; false |

The source-quality rereview for `1011d008` is published as `PASS` while
separately recording commit-policy `FAIL`; no native API effect was performed.
The `bfb86c12` merge has no source-tree difference from either parent. The
`486e81cd` task remains qualified with its product and consumer evidence but is
blocked on historical message disposition. None of those facts constitutes a
decision on the proposed dispositions.

## Portable Projection

- Source and portable copies of the policy, schema, checker, focused tests,
  generated standard, and reference documentation are byte-identical.
- `.aide/git/commit-message-dispositions.json` is absent from the portable
  payload, manifest, and checksums.
- `pack-status`, release validation, and release-draft validation pass with
  their retained no-publish boundaries.
- Six Q31 export-governance tests and 25 export/import consumer tests pass.

The projection/exclusion implementation is sound for the reviewed candidate;
the findings above are in the shared mechanism that is projected.

## Validation

- `py -3 -B .aide/scripts/tests/test_q27_commit_recovery.py -v`: PASS, 19/19.
- `py -3 -B .aide/scripts/tests/test_q31_export_pack_governance.py -v`: PASS, 6/6.
- `py -3 -B .aide/scripts/tests/test_export_import.py -v`: PASS, 25/25.
- `py -3 -B .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py pack-status`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py release validate`: PASS; no publish.
- `py -3 -B .aide/scripts/aide_lite.py release draft-validate`: PASS; no publish.
- Default and raw checks of the exact seven-commit task range: PASS, 7/7.
- `commit check --latest`: PASS for `dea2cf7f`.
- Default checks of all three proposal subjects: expected FAIL; proposal visible
  and ineffective.
- Raw checks of all three proposal subjects: expected FAIL with exact retained
  failures.
- Independent raw-object/hash recomputation: PASS for all three records.
- Replacement-ref adversarial fixture: FAIL, malformed commit incorrectly
  became raw `PASS`.
- Arbitrary-authority/future-date adversarial evaluation: FAIL, all three
  hypothetical accepted records became effective.
- Mixed-invalid-registry adversarial evaluation: FAIL, malformed adjacent and
  duplicate-id entries did not invalidate the registry.
- Exact full-range `git diff --check`: FAIL, two blank-at-EOF findings.

## Residual Risks And Boundaries

- No disposition was accepted or rejected by this review.
- No source, policy, task status, branch, ref, remote, target repository, tag,
  release, credential, or hosted setting was mutated.
- Tests used disposable repositories for all Git mutation.
- Latest/message-file/hook code paths remain separate from disposition loading;
  the reviewed defect is range traversal honoring replacement refs.
- Mechanism integration and all three exact decisions must remain blocked until
  the findings are repaired and independently re-reviewed.
