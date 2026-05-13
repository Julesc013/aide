# Q28 ExecPlan - Git Workflow Policy v0

## Purpose

Q28 is intended to define AIDE's branch roles, workflow detection rules, sync
and pruning posture, project workflow profiles, and report-only Git workflow
commands that future merge/land/promote helpers can consume.

## Scope

The planned scope includes Git workflow policies, branch-role and promotion
rules, sync and prune policies, `.aide/git/**` reports and profiles, AIDE Lite
`git` command surfaces, golden tasks, tests, export-pack integration,
documentation, and evidence.

## Non-Goals

- No branch creation, deletion, merge, push, rebase, prune, or remote mutation.
- No GitHub API or branch protection mutation.
- No provider, model, or network calls.
- No product runtime, Gateway forwarding, UI, Commander, mobile, MCP/A2A, or
  autonomous loop implementation.
- No mutation of Eureka, Dominium, or other external repositories.

## Allowed Paths

The authoritative allowlist is in `task.yaml`. This blocked packet edits only
the queue index and Q28 queue/evidence files.

## Current Facts

- Initial worktree was clean.
- Current branch is `main`.
- Current HEAD before Q28 blocker edits was
  `65689f6b0ca2b28b87cd289f049587e8f3b6970a`.
- Local branches: `main`.
- Remote branches: `origin/HEAD -> origin/main`, `origin/main`.
- No Git tags are present.
- Remote origin points at `https://github.com/Julesc013/aide.git`.
- `.aide.local/` is ignored.
- `py -3` is not available in this shell.
- `python` is Python 3.8.1; `python3` is Python 3.9.13.
- Q27 status is `blocked`.
- Q27 required policy and command outputs are absent.

## Blocker

Q28 cannot proceed under the prompt's prerequisite rule because Q27 outputs are
materially incomplete. Missing Q27 acceptance surfaces include:

- `.aide/policies/commit-messages.yaml`;
- `.aide/policies/task-resumption.yaml`;
- `.aide/policies/work-units.yaml`;
- `.aide/policies/recovery.yaml`;
- `.aide/hooks/commit-msg`;
- `.aide/git/commit-template.md`;
- `.aide/changelog/CHANGELOG.preview.md`;
- AIDE Lite `commit`, `changelog`, and `task` command families;
- Q27 golden tasks and tests;
- Q27 documentation and export-pack integration.

Q27 also stopped on the earlier Q25 pack/local-state blocker. That blocker is
still visible: AIDE Lite validation fails and pack-status does not pass.

## Recovery Plan

1. Repair Q25 pack/local-state baseline so AIDE Lite validation and pack-status
   reproduce a pass under the supported interpreter.
2. Reopen and implement Q27 commit discipline plus WorkUnit recovery.
3. Verify Q27 status reaches `needs_review` with policy, command, tests,
   docs, changelog preview, and export-pack outputs present.
4. Reopen Q28 and implement the full Git workflow policy layer.

## Validation Intent

After Q27 is repaired, Q28 should run the full validation suite from the prompt,
including AIDE Lite Git workflow commands, policy validation, golden tasks,
export-pack, pack-status, core test suites, and targeted secret scan.

## Evidence

Blocker evidence is stored under `evidence/`. No Q28 Git policy, command,
test, docs, or export-pack files were implemented.

## Retrospective

Q28 stopped before implementation to preserve queue ordering and avoid
silently implementing Q27 inside Q28.
