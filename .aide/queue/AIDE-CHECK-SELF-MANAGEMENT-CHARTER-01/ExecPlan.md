# ExecPlan: AIDE-CHECK-SELF-MANAGEMENT-CHARTER-01

## Objective

Check the AIDE self-management charter independently and stop at
`needs_review` with evidence.

## Scope

This is a check-only Track B governance task. It may create task-local evidence
and self-management check reports. It may update the queue index, latest task
packet, generated Task OS status reports, `PLANS.md`, and `IMPLEMENT.md`.

## Plan

1. Confirm clean preflight state and classify dirty state if present.
2. Read governing docs, queue truth, build task packet, build evidence, and
   Track B root/layout reports.
3. Check charter consistency, boundaries, evidence completeness, validation,
   and next-task routing.
4. Emit GovernanceFinding records as report convention only.
5. Validate JSON/YAML, report consistency, task evidence, broad repo state, and
   commit policy.
6. Stop at `needs_review`.

## Non-Goals

No schema implementation, CLI command implementation, GovernanceFinding helper
or library, OKF regeneration, generated-output ledger, doc truth reconciler,
file moves, renames, reference rewrites, migration apply, runtime, provider,
Gateway, GitHub, network, branch/worktree automation, push, merge, release, or
target-repo mutation.

## Exit Criteria

- Check reports and findings JSON exist and parse.
- Markdown and JSON reports agree on finding identifiers and routing.
- Build task evidence is complete.
- The check records `PASS_WITH_WARNINGS`.
- The recommended next task is `AIDE-ACCEPT-SELF-MANAGEMENT-CHARTER-01`.
