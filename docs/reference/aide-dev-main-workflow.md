# AIDE Dev/Main Workflow

Q30 applies the generic Q28/Q29 Git policy to the AIDE repository itself.

## Branch Roles

- `main`: canonical accepted truth for AIDE.
- `dev`: intended shareable integration branch, not canonical release truth.
- `task/*`, `codex/*`, `aide/*`, `fix/*`, and `repair/*`: bounded work branches
  that land to `dev`.
- `release/*`: future maintained release lines for public AIDE Lite, CLI, schema,
  or pack artifacts.
- `hotfix/*`: urgent repair branches with explicit backmerge expectations.

## Current AIDE Topology

Q30 local detection records:

- local `main` exists;
- `origin/main` exists;
- local `dev` does not exist;
- `origin/dev` does not exist;
- current branch is `main`, role `canonical`;
- no branch creation, push, merge, deletion, prune, or promotion was run.

The current plan is stored in `.aide/git/aide-dev-main-plan.json` and
`.aide/git/aide-dev-main-plan.md`.

## Future Dev Creation Plan

If AIDE adopts a live `dev` branch, a future reviewed queue item or explicit
operator action must run the helper plan and validation first. The recorded
future commands are examples of the intended operator action, not Q30 execution:

```powershell
git switch -c dev main
git push -u origin dev
```

Q30 deliberately does not run those commands.

## Promotion Gate

`dev -> main` promotion requires classified validation evidence:

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
- a targeted secret scan;
- a review packet and promotion evidence.

Warnings may be accepted only when evidence classifies them. `dev` must not be
treated as release truth.

## Inspection Commands

```powershell
py -3 .aide/scripts/aide_lite.py git detect
py -3 .aide/scripts/aide_lite.py git status
py -3 .aide/scripts/aide_lite.py git policy
py -3 .aide/scripts/aide_lite.py git plan
py -3 .aide/scripts/aide_lite.py git sync --dry-run
py -3 .aide/scripts/aide_lite.py git land --dry-run --target dev
py -3 .aide/scripts/aide_lite.py git promote --dry-run --from dev --to main
py -3 .aide/scripts/aide_lite.py git prune --dry-run
```

These commands remain local and non-mutating unless a future reviewed task
explicitly authorizes `--apply`. Q30 does not authorize `--apply` or `--push`.

## Export Boundary

The export pack carries the generic Q28/Q29 policies, project profiles, helper
docs, AIDE Lite command support, and tests. It does not export AIDE's live
`.aide/git/aide-dev-main-plan.*` as target-repo truth.

Q31 should synchronize the portable Git/commit workflow support for target repos
without copying AIDE-specific live branch state.
