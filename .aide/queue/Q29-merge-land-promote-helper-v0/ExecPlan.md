# Q29 ExecPlan - Merge Land Promote Helper v0

## Purpose

Q29 is intended to add the first AIDE Git helper layer for safe sync planning,
task-to-integration landing, integration-to-canonical promotion, and branch
prune guards.

## Scope

The planned implementation scope includes helper policy files under
`.aide/git/`, AIDE Lite `git sync`, `git plan`, `git land`, `git promote`, and
`git prune` commands, temporary Git fixture tests for mutating paths, golden
tasks, docs, export-pack integration, current-repo dry-run plans, and evidence.

## Non-Goals

- No live AIDE branch creation, deletion, merge, push, rebase, prune, or remote
  mutation.
- No GitHub API or branch protection mutation.
- No provider, model, or network calls.
- No product runtime, Gateway forwarding, UI, Commander, mobile, MCP/A2A, or
  autonomous loop implementation.
- No mutation of Eureka, Dominium, or other external repositories.

## Allowed Paths

The authoritative allowlist is in `task.yaml`. This blocked packet edits only
the queue index and Q29 queue/evidence files.

## Current Facts

- Initial worktree was clean.
- Current AIDE branch is `main`.
- Current HEAD before Q29 blocker edits was
  `1d9469676f162b5e729bc1e16536f9d5e328c815`.
- AIDE local branches: `main`.
- AIDE remote branches: `origin/HEAD -> origin/main`, `origin/main`.
- AIDE remote origin is `https://github.com/Julesc013/aide.git`.
- `.aide.local/` is ignored.
- `py -3` is unavailable.
- `python` is Python 3.8.1; `python3` is Python 3.9.13.
- Q27 status is `blocked`.
- Q28 status is `blocked`.
- Q27 and Q28 required output surfaces are absent.

## Blocker

Q29 cannot proceed under the prompt's prerequisite rule because both
prerequisite phases are materially incomplete:

- Q27 did not add commit discipline, changelog preview, WorkUnit recovery, task
  recovery commands, golden tasks, tests, docs, or export-pack integration.
- Q28 did not add Git workflow policy, branch-role policy, promotion/sync/prune
  policy, project profiles, workflow detection artifacts, AIDE Lite `git`
  commands, golden tasks, tests, docs, or export-pack integration.
- AIDE Lite validation and pack-status still fail on the earlier Q25
  pack/local-state baseline issue.

## Recovery Plan

1. Repair Q25 pack/local-state baseline so AIDE Lite validation and pack-status
   reproduce a pass under a supported interpreter.
2. Reopen and implement Q27 commit discipline plus WorkUnit recovery.
3. Reopen and implement Q28 Git workflow policy plus report-only detection.
4. Reopen Q29 and implement dry-run helpers with mutating paths tested only in
   temporary fixture repositories.

## Validation Intent

After Q27 and Q28 are repaired, Q29 should run the full validation suite from
the prompt, including Git helper dry-runs, fixture land/promote/prune tests,
golden tasks, export-pack, pack-status, core test suites, and targeted secret
scan.

## Evidence

Blocker evidence is stored under `evidence/`. No Q29 helper policy, command,
test, docs, generated helper plan, or export-pack files were implemented.

## Retrospective

Q29 stopped before implementation to preserve queue ordering and avoid
silently implementing Q27 or Q28 inside Q29.
