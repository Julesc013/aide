# Q27 Commit Discipline Report

Status: COMPLETE FOR REVIEW.

## Policy

- Policy path: `.aide/policies/commit-messages.yaml`.
- Standard path: `.aide/reports/aide-commit-message-standard.md`.
- Commit template: `.aide/git/commit-template.md`.
- Hook template: `.aide/hooks/commit-msg`.
- Standard: Conventional Commits subject plus required structured Markdown body.
- Required headings: `## Summary`, `## Why`, `## Changed`, `## Validation`, `## Changelog`, `## Risks`, `## Follow-up`.
- Changelog categories: Added, Changed, Fixed, Removed, Deprecated, Security, Docs, Tests, Internal, Risks, Follow-up.
- Trailers: `AIDE-Task`, `AIDE-Phase`, `AIDE-Result`, `AIDE-Scope`, `AIDE-Token-Impact`, `AIDE-Quality-Gate`.

## Command Behavior

- `commit check --message-file PATH`: validates subject, body headings, validation tokens, changelog categories, trailers, and obvious secret/raw prompt markers.
- `commit check --message TEXT`: validates inline message fixtures for tests and local use.
- `commit check --latest`: reads `git log -1 --pretty=%B` and validates the latest commit.
- `commit check --range BASE..HEAD`: validates every commit returned by the range.
- `commit template`: prints `.aide/git/commit-template.md`.
- `commit status`: reports policy/template/hook presence, local hooksPath state, and latest commit result.
- `commit install-hook`: explicit opt-in command only; configures `core.hooksPath=.aide/hooks` when run by an operator. Q27 did not run it.

## Validation Result

- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS on the latest Q27 documentation commit.
- `py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD`: PASS on the first five Q27 commits.
- `py -3 .aide/scripts/aide_lite.py commit status`: PASS; policy, template, and hook template exist; local `core.hooksPath` is unset.
- `py -3 .aide/scripts/aide_lite.py commit template`: PASS; prints required body headings and trailers.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q27_commit_recovery.py`: PASS, 14 tests.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 10/10 golden tasks.

## Commit Sequence

- `57b73ba chore(aide): add Q27 commit and recovery governance packet`
- `86974c9 policy(aide): define structured commits and WorkUnit recovery`
- `2146efa feat(aide-lite): add commit and task recovery commands`
- `f97d773 test(aide): cover commit lint and WorkUnit recovery`
- `0de5071 docs(aide): document commit discipline and recovery workflows`

The final export/evidence commit is made after this evidence file is written and is checked separately before final reporting.

## Limitations

- Existing pre-Q27 commits are not rewritten. They are reported as malformed by changelog preview/range checks when included in a range.
- Local hook installation is opt-in and was not applied to `.git/hooks`.
- Commit checking is deterministic local parsing; it does not infer semantic release impact beyond structured body categories.
