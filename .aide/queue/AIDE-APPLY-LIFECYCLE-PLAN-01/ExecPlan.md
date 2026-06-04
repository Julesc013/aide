# AIDE-APPLY-LIFECYCLE-PLAN-01 ExecPlan

## Purpose

Create a planning-only lifecycle proof ladder after `AIDE-APPLY-02 - Scoped Transaction Executor v0` was accepted with notes and Task OS current/latest reporting was repaired. This task does not implement or execute lifecycle apply.

## Scope

Allowed writes are limited to the task directory, `.aide/queue/index.yaml`, `.aide/context/latest-task-packet.md`, selected Task OS generated reports, and README next-work text. No implementation files, lifecycle model roots, target repositories, release files, provider/Gateway files, docs/reference files, branches, worktrees, or network surfaces are authorized.

## Milestones

1. Verify live preconditions and record gate evidence.
2. Create lifecycle plan task scaffold.
3. Define capability reality for each lifecycle surface.
4. Define the lifecycle proof ladder.
5. Define install, upgrade, lifecycle repair, rollback, uninstall, active repo, target adoption, and token/quality ledger interlocks.
6. Select exactly one next WorkUnit without executing it.
7. Write lifecycle graph, evidence, validation, and review packet.
8. Refresh authorized Task OS reports and run validation.
9. Commit if validation passes or warnings are classified, then stop at `needs_review`.

## Non-Goals

- No lifecycle apply execution.
- No install apply implementation or execution.
- No upgrade apply implementation or execution.
- No lifecycle repair apply implementation or execution.
- No rollback/uninstall implementation or execution.
- No active AIDE repo apply.
- No target repo mutation.
- No branch/worktree mutation.
- No merge, push, promotion, release publication, or GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply.
- No production-ready or release-ready capability claim.

## Review Gate

End at `needs_review`. The selected next task is `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`, a planning/schema/fixture-shape WorkUnit. It must not execute lifecycle apply.
