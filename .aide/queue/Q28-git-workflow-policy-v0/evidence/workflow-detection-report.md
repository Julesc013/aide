# Q28 Workflow Detection Report

## Current Repo Detection

- command: `py -3 .aide/scripts/aide_lite.py git detect`
- result: PASS
- report JSON: `.aide/git/workflow-detection.json`
- report Markdown: `.aide/git/workflow-detection.md`
- current branch: `main`
- current commit recorded in report: `c305b581855ab0d5ca722f8aae27a1ee1fe2b11f`
- current branch role: `canonical`
- detected workflow: `trunk_without_dev`
- confidence: `medium`
- canonical branch: `main`
- integration branch detected: `false`
- local branches: `main`
- remote branches: `origin/main`
- tags: none
- recommended next action: classify dirty tree before branch-sensitive work

## Warnings

- `dirty_tree_detected`: expected during Q28 implementation and artifact regeneration.
- `integration_branch_dev_missing`: no local or remote `dev` branch is present in this repo snapshot.

## No-Mutation Confirmation

The command reads local Git state with report-only operations:

- current branch
- current commit
- local branches
- remote branch refs
- tags
- remote URL summary
- worktree status

It does not fetch, create branches, delete branches, merge, rebase, prune, push,
call GitHub APIs, call providers/models, or use outbound network services.
