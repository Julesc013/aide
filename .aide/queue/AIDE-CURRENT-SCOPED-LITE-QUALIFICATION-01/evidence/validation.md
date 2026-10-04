# Current qualification validation — 2026-10-05

## Actual behavioral checks

These commands ran inside admitted CodexSandboxOffline jobb92f98a4 with exact
source-input hashes recorded in source-qualification.json:

- `python -B -m unittest discover -s .aide/scripts/tests -p test_stable_release_admission.py`:5 passed.
- `python -B -m unittest discover -s .aide/scripts/tests -p test_public_archive_fixture.py`:8 passed, no skips.
- `python -B -m unittest discover -s .aide/scripts/tests -p "test_q4[78]*.py"`:36 passed, no skips.
- `python -B .aide/scripts/aide_lite.py export-pack`:exit0.
- `python -B .aide/scripts/aide_lite.py validate`:exit0, full logs retained.

Separate pinned export supervision ran `release stable-build --version 1.0.0`
and `release stable-validate --version 1.0.0`:PASS/retired. Source36 proof was
reused by exact hashes at build time. All8 current-byte consumer cases passed
exactly once;38 forms/39 raw command outputs plus12 raw job observations, Task
OS and four-asset identical replay verified. Original entry7b2c4eba passed its
native exact config/asset/inspect probe, collection and retirement.71 unchanged
core/host checks are reused qualified evidence, not a rerun in this closeout.

Source/local build1813, consumer envelopeb96d, artifact/pin5d and integration21
received exact independent ACCEPT_WITH_NOTES; all notes nonblocking/disposed.
Main/dev/task atomic synchronization passed;88 pairs match/85 other tips stay.

## Record-only and checkout checks

- `py -3 -B scripts/aide compile --dry-run`:only existing generated manifest would change; managed sections/manual content untouched.
- `py -3 -B scripts/aide compile --write`:only manifest changed; deferred outputs remain deferred.
- `py -3 -B scripts/aide validate`:PASS,149 info/zero warnings/errors; structural scope, not full YAML schemas or behavior.
- Existing `verify_task_packet`:all required headings/refs present; no warning/error;1079 document-size tokens at that check, not actual host usage.
- `task inspect --task-id AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01`:complete,missing_evidence0,noop_already_complete.
- `git diff --check`:PASS. Generated CRLF recognition preserves the three default whitespace checks; no suppression.
- `pack-status`:initial postintegration FAIL on four CRLF-to-LF checkout mismatches; after bounded exact archive restoration PASS_SOURCE_ANCESTOR,checksums/boundary PASS with zero problems.
- All846 working checksums,24 supervisor pins and four stable asset hashes verified. Staged846 exact Git blob check passed; final structured commit/ref review precedes effects and terminal records remain separate.

The generated subtree-only -text override prevents recurrence. Four raw archive
members equal the qualified checksum identity; root source/Git LF forms are
newline-equivalent. Frozen source proof keeps its actual executed raw hashes.
No archive, source behavior, assertion, usage coverage or supervisor changed.

## Preserved failures and limitations

Original preparation records remain in Git history. Failed27de35f9 admission,
46e91fbf private-temp validation/recovery, wrong-SID observations,33662de9 dirty-
source preflight and the checkout checksum failure retain exact evidence; none
is relabelled PASS. Actual current proof/reviews/receipts supersede only pending
preparation statements. Outer/client/read containment, hard quota, ten historical
owner decisions, live/matched efficiency, stable publication/downloaded assets,
adoption and wider unknown disk cleanup remain unqualified. No model invocation,
new worktree, replacement archive, machine policy or unknown cleanup occurred.
