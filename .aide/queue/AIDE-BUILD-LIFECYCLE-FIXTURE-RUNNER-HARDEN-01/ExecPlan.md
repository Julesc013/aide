# ExecPlan

## Objective

Harden the reviewed lifecycle fixture temp runner without widening authority.

## Scope

The hardening slice may update `core/apply/lifecycle_fixture_runner.py` and
focused tests in `.aide/scripts/tests/test_aide_lifecycle_fixture_runner.py`.
It may write task evidence and regenerate lifecycle fixture runner reports.

## Non-Goals

- No service, Commander, provider adapter, branch/worktree, release, GitHub,
  Gateway, network, or model/provider work.
- No target repo apply, active repo apply, rollback execution, uninstall
  execution, or broad lifecycle apply.
- No full schema suite or plugin framework.

## Plan

1. Add direct regression coverage for unsupported operation and malformed plan paths.
2. Harden `verify` report truth checks for overclaiming and rollback record content.
3. Add malformed marker/report failure tests where practical.
4. Rerun focused and relevant validation.
5. Write evidence and stop at `needs_review`.

## Progress

- [x] CHECK-01 verified behavior and selected HARDEN-01.
- [x] HARDEN-01 queue scaffold created.
- [x] Runner hardening implemented.
- [x] Focused tests expanded.
- [x] Validation complete.
- [x] Evidence written.
- [x] Status moved to `needs_review`.

## Retrospective

HARDEN-01 adds stricter verification of required run-report fields, forbidden
readiness/apply/rollback true flags, rollback-compatible record parsing, and
rollback record truth. Focused tests now cover unsupported operation and
malformed plan rejection, overclaiming fail-closed behavior, malformed rollback
records, missing required run fields, empty/wildcard path-jail cases, and
missing managed-section marker failure.

## Recovery

If interrupted, inspect `status.yaml`, current diff, and the focused test file
before continuing. Do not widen beyond lifecycle fixture temp-runner hardening.
