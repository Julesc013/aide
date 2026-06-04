# AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01 ExecPlan

## Purpose

Define the lifecycle schema and fixture-shape layer required before any future fixture install, upgrade, lifecycle repair, rollback, or uninstall proof. This task is planning and schema work only.

## Scope

Allowed writes are limited to this task directory, lifecycle schema files under `.aide/apply/`, lifecycle examples under `.aide/examples/apply/lifecycle/`, the lifecycle schema reference doc, queue index, latest task packet, README next-work text, and generated status reports from validation commands. No implementation files, target repositories, release files, provider/Gateway files, branch/worktree automation, or lifecycle apply surfaces are authorized.

## Milestones

1. Verify live preconditions from queue, AIDE-APPLY-02 accepted-with-notes state, and validation commands.
2. Create this queue scaffold and explicit allowed-path packet in `task.yaml`.
3. Define lifecycle artifact model.
4. Create lifecycle manifest, plan, report, and rollback-compatible record schemas.
5. Create non-mutating lifecycle examples.
6. Define fixture repository shape without materializing fixture target files.
7. Define scoped transaction executor interlock and v0 gaps.
8. Define validation design and token/quality ledger hook.
9. Select exactly one next WorkUnit without executing it.
10. Run validation, write evidence, commit, and stop at `needs_review`.

## Non-Goals

- No lifecycle apply implementation or execution.
- No install apply implementation or execution.
- No upgrade apply implementation or execution.
- No lifecycle repair apply implementation or execution.
- No rollback or uninstall implementation or execution.
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

End at `needs_review`. The selected next task is `AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01`, a local schema/example validation WorkUnit. It must not execute lifecycle apply.
