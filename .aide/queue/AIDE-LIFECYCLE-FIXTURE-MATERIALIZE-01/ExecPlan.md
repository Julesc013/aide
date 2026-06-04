# AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01 ExecPlan

## Purpose

Materialize static lifecycle fixture inputs and expected-state artifacts for future lifecycle dry-run proof tasks. This WorkUnit creates checked-in fixture content only; it does not implement or execute lifecycle apply.

## Scope

Allowed writes are limited to this task directory, `.aide/examples/apply/lifecycle-fixtures/**`, `.aide/reports/lifecycle-fixtures/**`, deterministic validation/status report refreshes required by this prompt, `.aide/queue/index.yaml`, and `.aide/context/latest-task-packet.md`.

The fixture root is `.aide/examples/apply/lifecycle-fixtures/`. The fixture report root is `.aide/reports/lifecycle-fixtures/`.

## Milestones

1. Verify upstream validator, lifecycle schemas, fixture plan, accepted scoped executor chain, and report-only status commands.
2. Create the queue scaffold and explicit allowed-path packet for this WorkUnit.
3. Materialize static source-pack files, target baselines, expected states, blocked-state metadata, expected reports, and rollback-compatible record examples.
4. Record deterministic SHA-256 hashes for checked-in fixture content where expected reports and rollback records reference preimages or postimages.
5. Write task-local evidence for preconditions, materialization, fixture validation, hashes, boundaries, changed files, remaining risks, and the next task.
6. Run lifecycle-schema validation, parse checks, boundary searches, changed-file secret scan, and queue/status validation.
7. Commit the completed queue task and stop at `needs_review`.

## Non-Goals

- No lifecycle apply implementation or execution.
- No scoped transaction apply against fixture targets.
- No active repo scoped apply mutation.
- No install apply, upgrade apply, lifecycle repair apply, rollback apply, or uninstall apply implementation or execution.
- No target repo mutation.
- No branch/worktree mutation, merge, push, promotion, release publication, or GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply, broad deletes, or broad moves.
- No production-ready or release-ready claim.

## Fixture Classes

- baseline files
- generated files
- managed-section files
- manual content files
- protected path attempts represented as metadata
- drifted files
- missing-marker files
- duplicate-marker files
- malformed-marker files
- nested-marker files
- upgrade baseline and desired state
- uninstall expected state
- rollback-compatible record examples

## Review Gate

End at `needs_review`. The selected next task is `AIDE-LIFECYCLE-FIXTURE-CHECK-01`, an independent review of fixture materialization and validator coverage before dry-run plan generation.
