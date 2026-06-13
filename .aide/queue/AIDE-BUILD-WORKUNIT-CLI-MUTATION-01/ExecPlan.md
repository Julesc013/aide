# AIDE-BUILD-WORKUNIT-CLI-MUTATION-01 ExecPlan

## Objective

Build the first WorkUnit queue metadata mutation CLI slice: create queued WorkUnits from bounded specs, block queued WorkUnits with reason/note, and attach safe evidence pointers.

## Scope

- Keep implementation in `core/protocol/workunit_cli.py`.
- Keep `.aide/scripts/aide_lite.py` as CLI dispatch and output only.
- Add focused tests in `.aide/scripts/tests/test_aide_workunit_cli_mutation.py`.
- Write reports under `.aide/reports/workunit-cli-mutation/`.

## Validation

Run focused mutation tests, predecessor tests, WorkUnit CLI commands, compatibility commands, repo validation, and commit policy checks.

## Result

Implemented and validated. Command evidence is in `.aide/reports/workunit-cli-mutation/command-results.json`; mutation safety evidence is in `.aide/reports/workunit-cli-mutation/mutation-safety.json`.

## Stop State

Stop at `needs_review`. Do not implement claim, run, finish, repair, leases, scheduler, Test Broker, Service, Commander, providers, branch/worktree automation, repo apply, rollback, release, network, Gateway, GitHub, or model/provider calls.
