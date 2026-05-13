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

The authoritative allowlist is in `task.yaml`. Q28 edits stayed inside the
policy, `.aide/git/`, AIDE Lite, test, golden-task, documentation, export-pack,
context-packet, and queue/evidence paths authorized there.

## Current Facts

- Initial Q28 redo worktree was clean except baseline `changelog preview`
  regenerated Q27 preview files before edits.
- Current branch is `main`.
- Current HEAD before Q28 edits is
  `600c5fb2e61b517da5276145500631e9f0ee16aa`.
- Local branches: `main`.
- Remote branches: `origin/HEAD -> origin/main`, `origin/main`.
- No Git tags are present.
- Remote origin points at `https://github.com/Julesc013/aide.git`.
- `.aide.local/` is ignored.
- Q27 status is `needs_review` and Q27 policy/command surfaces are present.

## Implementation Plan

1. Reopen Q28 packet and record baseline validation.
2. Add Git workflow, branch roles, promotion, sync, and prune policies.
3. Add `.aide/git/**` report/docs/profile artifacts.
4. Extend AIDE Lite with report-only `git` workflow commands.
5. Add deterministic golden tasks and unittest coverage.
6. Update WorkUnit/commit integration, docs, command catalog, and export pack.
7. Generate current workflow detection artifacts and Q29 task packet.
8. Write final evidence and stop at `needs_review`.

## Validation Intent

Q28 should run the full validation suite from the prompt, including AIDE Lite
Git workflow commands, policy validation, golden tasks, export-pack,
pack-status, core test suites, and targeted secret scan.

## Evidence

Implementation evidence is stored under `evidence/`. Superseded blocker
findings are replaced by this redo pass.

## Retrospective

Q28 implemented the policy and detection layer and stopped at `needs_review`.
`git detect`, `git doctor`, `git status`, `git workflow`, `git roles`, and
`git policy` are report-only. Merge, land, promote, prune, push, GitHub
protection, and CI application helpers remain deferred to later phases.

Final validation found and fixed one selftest fixture issue: the temp fixture
copied new Q28 golden tasks without copying the Q28 policy files. The fixture
now copies `Q28_REQUIRED_FILES`, and AIDE Lite `test`, `selftest`, raw
`.aide/scripts/tests`, Harness, Gateway, Compatibility, and Provider tests pass.
