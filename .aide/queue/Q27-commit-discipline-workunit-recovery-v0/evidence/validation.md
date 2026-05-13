# Q27 Validation

Status: IN PROGRESS.

## Baseline Before Q27 Edits

- `git status --short`: PASS; worktree initially clean.
- `git branch --show-current`: PASS; `main`.
- `git rev-parse HEAD`: PASS; `05330b0842a3e39487bb67d8d8b44b4c40902ad7`.
- `git check-ignore .aide.local/`: PASS; `.aide.local/` is ignored.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; existing queue review-gate warnings.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; existing queue review-gate warnings.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; Q25/Q26 review and Q27 redo recommendation.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; generated pack artifacts.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; provenance result `DIRTY_SOURCE_RECORDED`.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS.
- `py -3 -m unittest discover -s .aide/scripts/tests`: TIMED OUT during baseline run; canonical `py -3 .aide/scripts/aide_lite.py test` passed.

## Final Validation

- `git status --short`: PASS; expected Q27 generated/evidence/export changes before final commit.
- `git diff --check`: PASS_WITH_LINE_ENDING_WARNINGS; no whitespace errors, Git reported Windows CRLF normalization warnings for modified generated/text files.
- `git branch --show-current`: PASS; `main`.
- `git rev-parse HEAD`: PASS; latest checked pre-final evidence commit was `0de5071ded874d71bf35c3c00a9b0daf3ab83899`.
- `git check-ignore .aide.local/`: PASS; `.aide.local/`.
- `py -3 scripts/aide validate`: PASS_WITH_WARNINGS; 148 info, 7 warnings, 0 errors. Warnings are existing review gates plus stale generated manifest source fingerprint.
- `py -3 scripts/aide doctor`: PASS_WITH_WARNINGS; same Harness warnings and `next_recommended_step: Q25 review`.
- `py -3 scripts/aide self-check`: PASS_WITH_WARNINGS; same wider queue-state warnings and generated manifest drift. Q27 does not override earlier review gates.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py selftest`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS; 10/10 golden tasks.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD`: PASS; five Q27 commits checked.
- `py -3 .aide/scripts/aide_lite.py commit template`: PASS; printed structured template.
- `py -3 .aide/scripts/aide_lite.py commit status`: PASS; policy/template/hook template present, local hooksPath unset.
- `py -3 .aide/scripts/aide_lite.py changelog preview`: PASS_WITH_WARNINGS; default range included older pre-Q27 malformed commits and reported them.
- `py -3 .aide/scripts/aide_lite.py changelog preview --range HEAD~5..HEAD`: PASS; five Q27 commits, zero malformed.
- `py -3 .aide/scripts/aide_lite.py task inspect`: PASS; compact Q28 id resolved to `Q28-git-workflow-policy-v0`, superseded/partial.
- `py -3 .aide/scripts/aide_lite.py task noop-check`: PASS; report-only, no mutation.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id Q27-commit-discipline-workunit-recovery-v0`: PASS; Q27 classified complete at `needs_review` with seven evidence files.
- `py -3 .aide/scripts/aide_lite.py task noop-check --task-id Q27-commit-discipline-workunit-recovery-v0`: PASS; `noop_already_complete`, no mutation.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; 32 queue entries.
- `py -3 .aide/scripts/aide_lite.py task dependencies`: PASS; Q28 depends on Q27.
- `py -3 .aide/scripts/aide_lite.py task evidence`: PASS; Q28 evidence listed.
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`: PASS; 144 included files, 147 checksums, boundary PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS; checksums valid, boundary PASS, provenance `DIRTY_SOURCE_RECORDED`.
- `py -3 .aide/scripts/aide_lite.py pack --task "Q28 Git Workflow Policy v0"`: PASS; `.aide/context/latest-task-packet.md`, 3,664 chars, 916 approximate tokens.
- `py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md`: PASS; 916 approximate tokens, within budget.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q27_commit_recovery.py`: PASS; 14 tests.
- `py -3 .aide/scripts/tests/test_golden_tasks.py -v`: PASS; 9 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS; 133 tests.
- `py -3 -m unittest discover -s core/harness/tests -t .`: PASS; 27 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .`: PASS; 5 tests.
- `py -3 -m unittest discover -s core/gateway/tests -t .`: PASS; 9 tests.
- `py -3 -m unittest discover -s core/providers/tests -t .`: PASS; 8 tests.
- Targeted `rg` secret scan: PASS_AFTER_INSPECTION. Matches were policy/test/template/path terms such as `TOKEN`, `api_key`, `SECRET_PATTERNS`, `sk-ant` regex text, and `latest-task-packet`; no actual provider key, `.env` content, `.aide.local` state, private key, raw prompt, or raw response was found.

## Resolved During Final Validation

- Raw `.aide/scripts/tests` initially failed because the new `changelog_preview_golden` warned when a minimal fixture lacked pre-generated preview files and because the legacy golden-task test expected six tasks. Q27 now uses a deterministic changelog fixture and updates the test to accept the expanded catalog; full discovery now passes.
- `task inspect` initially treated compact packet id `Q28` as a missing queue directory. Q27 now resolves short ids from `.aide/queue/index.yaml`, and the behavior is covered by `test_task_short_id_resolves_from_queue_index`.

## Remaining Warnings Outside Q27 Scope

- Harness review-gate warnings for older queue items remain.
- `.aide/generated/manifest.yaml` source fingerprint is stale. The Harness recommends `scripts/aide compile --write`; that would modify generated-artifact surfaces outside Q27 allowed paths.
- `scripts/aide self-check` continues to recommend Q25 review from the broader queue state. Q27 records this honestly rather than overriding earlier gates.
