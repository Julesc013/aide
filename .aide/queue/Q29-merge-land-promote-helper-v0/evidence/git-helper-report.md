# Q29 Git Helper Report

## Implemented Helper Commands

- `git plan`: reads local Git state and writes `.aide/git/latest-helper-plan.json` plus `.aide/git/latest-helper-plan.md`.
- `git sync --dry-run`: reports whether a fast-forward-only sync would be appropriate.
- `git land --dry-run --target dev`: reports a task-to-integration landing plan.
- `git promote --dry-run --from dev --to main`: reports an integration-to-canonical promotion plan.
- `git prune --dry-run`: reports branch-prune eligibility using ancestor containment.

Each command is dry-run/report-only by default. `--apply` exists for later explicit operator use and fixture tests. `--push` is explicit and is blocked for Q29 apply behavior.

## Safety Model

The helper model inspects:

- repo root detection;
- current branch and commit;
- dirty tree state;
- local and remote branches;
- upstream and ahead/behind status where available;
- Q28 branch-role classification;
- protected roles: canonical, integration, release, deploy;
- policy-file presence;
- ancestor containment for prune candidates;
- unpushed protected branch status where upstream data exists.

If Git state is unavailable or uncertain, helper plans become conservative and block mutation.

## Current Live Repo Plan

- Current branch: `main`.
- Current branch role: `canonical`.
- Detected workflow: `trunk_without_dev`.
- Integration branch: not detected locally or remotely.
- Worktree: dirty because Q29 generated artifacts/evidence are pending commit.
- Upstream: `origin/main`.
- Ahead/behind: ahead 16, behind 0 at plan generation.
- Plan status: `blocked`.
- Blocker: `dirty_tree_requires_classification`.
- Warnings: `dirty_tree_detected`, `integration_branch_dev_missing`.
- Remote mutation: `false`.
- Force push allowed: `false`.
- Executed commands in latest plan: none.

This is the expected live-repo behavior for a policy/helper implementation phase on `main`: report the state, block branch-sensitive mutation, and stop at review.

## Dry-Run Results

- `git sync --dry-run`: blocked for apply by dirty tree, but only planned `git status --short` and `git pull --ff-only`.
- `git land --dry-run --target dev`: blocked because source role is canonical/protected, tree is dirty, and `dev` is missing.
- `git promote --dry-run --from dev --to main`: blocked because `dev` is missing and tree is dirty.
- `git prune --dry-run`: ready dry-run; current/protected `main` is not eligible.

## Limitations

- Q29 does not create the AIDE `dev` branch.
- Q29 does not promote or merge live AIDE branches.
- Q29 does not push to any remote.
- Q29 does not apply GitHub protection or CI.
- Validation evidence is recommended by helper plans, but helper commands do not automatically run heavy validation suites unless a later phase explicitly extends them.
