# Q30 Dev/Main Policy Report

## Policy Artifact

- Path: `.aide/git/aide-branch-policy.yaml`
- Schema: `aide.repo-branch-policy.v0`
- Repo id: `julesc013/aide`
- Status: active

## Branch Semantics

- `main`: canonical accepted truth.
- `dev`: intended shareable integration truth.
- `dev` canonical truth: false.
- `dev` release truth: false.
- `task/*`, `codex/*`, `aide/*`, `fix/*`, and `repair/*`: bounded work branches that land to `dev`.
- `review/*`: review staging.
- `release/*`: future maintained release line only when shipped AIDE Lite/CLI/schema lines exist.
- `hotfix/*`: urgent repair branch with explicit backmerge expectations.

## Live Mutation Rule

Q30 does not mutate live branches. It does not create, push, merge, promote,
prune, delete, fetch, tag, or call GitHub. Missing `dev` is handled as a
future explicit operator plan, not an automatic repair.

## Promotion Gate

The AIDE `dev -> main` gate requires:

- `py -3 scripts/aide validate`
- `py -3 scripts/aide doctor`
- `py -3 scripts/aide self-check`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py test`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 .aide/scripts/aide_lite.py eval run`
- `py -3 .aide/scripts/aide_lite.py commit check --range <base>..<head>`
- `py -3 .aide/scripts/aide_lite.py changelog preview`
- `py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0`
- `py -3 .aide/scripts/aide_lite.py pack-status`
- targeted secret scan
- review packet and promotion evidence

## Validation

- `py -3 .aide/scripts/aide_lite.py git policy`: PASS.
- `py -3 .aide/scripts/aide_lite.py eval run`: PASS, 22/22 golden tasks.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_q30_aide_dev_main_policy.py`: PASS, 9 tests.
