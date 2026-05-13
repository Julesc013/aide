# Q29 Fixture Merge Report

## Fixture Test Command

- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q29_git_helper.py`: PASS, 14 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests`: PASS, 155 tests.

All local Git mutation tests used temporary repositories. Fixture repositories configured `user.name` and `user.email` locally inside the temp directory only.

## Covered Scenarios

- Task branch lands to `dev`: PASS. A temp repo created `main`, `dev`, and `task/example`; dry-run produced a plan; fixture `--apply` merged the task commit into `dev`.
- `dev` promotes to `main`: PASS. A temp repo created `main` and `dev`; dry-run produced a plan; fixture `--apply` merged the dev commit into `main`.
- Contained branch prune: PASS. A contained task branch was eligible in dry-run and deleted by fixture-only `--apply`.
- Unmerged branch refusal: PASS. A branch not contained in `dev` or `main` was not eligible for prune.
- Protected branches: PASS. `main`, `dev`, `release/*`, and `gh-pages` were never eligible for pruning.
- Dirty tree blocks mutation: PASS. Fixture dirty tree blocked land/promote apply behavior.
- Unknown branch role is conservative: PASS. Unknown source role blocked land mutation.
- No remote push: PASS. No push command executes unless explicitly requested; Q29 apply blocks remote push.
- No force push: PASS. Helper execution rejects force-push command shapes.
- JSON and Markdown shape: PASS. Helper plan reports include schema, non-mutating marker, commands, status, blockers, warnings, and state.

## Live Repo Boundary

The live AIDE repository only ran dry-run helper commands. No live branch creation, checkout mutation, merge, deletion, prune, push, fetch, tag, or release command was run.
