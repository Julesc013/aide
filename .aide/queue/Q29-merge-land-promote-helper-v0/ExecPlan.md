# Q29 ExecPlan - Merge Land Promote Helper v0

## Purpose

Q29 adds the first AIDE Git helper layer for safe sync planning, task-to-dev
landing, dev-to-main promotion planning, and branch pruning guards.

The implementation must make the safe path obvious while keeping dangerous
operations hard: live AIDE branch work remains dry-run/report-only in Q29, and
all mutating helper paths are exercised only in temporary fixture repositories.

## Scope

- Reopen the existing Q29 queue packet from its superseded blocker state.
- Add `.aide/git/helper-policy.yaml` and `.aide/git/helper-commands.md`.
- Add generated current-repo helper plans at `.aide/git/latest-helper-plan.*`.
- Extend AIDE Lite with:
  - `git plan`
  - `git sync`
  - `git land`
  - `git promote`
  - `git prune`
- Build a reusable conservative Git safety model.
- Add fixture tests that create temporary Git repositories and apply local
  merges/deletes only inside those fixtures.
- Add Q29 golden tasks.
- Update docs, AGENTS guidance, export pack, and evidence.

## Non-Goals

- No live AIDE branch creation, deletion, merge, push, prune, rebase, or fetch.
- No remote push anywhere.
- No GitHub API mutation or branch protection automation.
- No CI workflow creation.
- No provider/model/network calls.
- No product runtime, Gateway forwarding, Commander, UI, mobile, MCP/A2A, or
  autonomous loop work.

## Dependencies

- Q27 commit discipline and WorkUnit recovery: present and needs_review.
- Q28 Git workflow policy and report-only detection: present and needs_review.
- Current repo branch topology: local `main`, remote `origin/main`, no local
  or remote `dev`.

## Implementation Steps

1. Record baseline Git and validation state.
2. Reopen Q29 packet and update queue index.
3. Add helper policy/docs and Q29 required file validation anchors.
4. Implement Git safety collection, dry-run plan rendering, sync/land/promote
   planning, prune eligibility, and fixture-only apply behavior.
5. Add tests for dry-run and fixture apply scenarios.
6. Add golden tasks and catalog entries.
7. Regenerate helper plan, changelog previews, export pack, and Q30 task
   packet.
8. Write evidence and set Q29 to `needs_review`.
9. Run validation and commit each coherent slice using Q27 structured commit
   discipline.

## Validation Intent

- AIDE Harness validate/doctor/self-check.
- AIDE Lite validate/test/selftest/eval run.
- AIDE Lite `git detect/doctor/status/policy/plan/sync/land/promote/prune`.
- Targeted Q29 unit tests for fixture land/promote/prune behavior.
- Core Harness/Compat/Gateway/Provider unit tests.
- Export-pack and pack-status.
- Commit latest/range checks.
- Changelog preview.
- Secret scan.

## Review Gate

Q29 must end at `needs_review`, not `passed`.
