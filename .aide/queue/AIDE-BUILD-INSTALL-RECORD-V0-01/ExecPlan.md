# ExecPlan: AIDE-BUILD-INSTALL-RECORD-V0-01

## Objective

Build InstallRecord v0 as a no-apply protocol, helper, projection, validation, fixture, report, and CLI slice.

## Scope

This task may add the InstallRecord schema, shared helper, focused tests, fixtures, reports, CLI commands, queue packet, evidence, queue index entry, and root planning/execution logs.

It may not implement install apply, update apply, migration apply, rollback apply, uninstall apply, target scanning, target mutation, release archive creation, tags, uploads, GitHub Releases, provider/model/network calls, runtime, Workbench, Commander, Omnigent, or branch/worktree automation.

## Plan

1. Confirm wave truth and accepted predecessor objects.
2. Add the InstallRecord v0 schema.
3. Add `core/protocol/install_record.py` with deterministic projection, digesting, validation, fixture generation, and reports.
4. Add `install-record status/project/validate` CLI commands.
5. Add focused fixture and CLI tests.
6. Run validation and record evidence.
7. Stop at `needs_review` and recommend `AIDE-CHECK-INSTALL-RECORD-V0-01`.

## Validation

Run JSON parse, compileall, focused tests, InstallRecord status/project/validate, predecessor regressions, Q43-Q48 no-apply/no-publish validators, broad validation, task inspect/evidence, safety scans, diff checks, and commit-policy check.
