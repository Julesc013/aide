# Validation

Preflight commands run before task artifact writes:

- `git status --short --branch`: PASS, `## main...origin/main`
- `git remote -v`: PASS, origin fetch/push configured.
- `git rev-parse HEAD`: PASS, `879ad2b7594f52cc8b0d83c174bc4c62a1f8d923`
- `git show --stat --oneline --name-status HEAD`: PASS, prior commit was `audit(aide): checkpoint rollback record evidence`.
- `git diff --check HEAD^ HEAD`: PASS, no whitespace errors.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, latest task before this WorkUnit was `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS, global selector still returned `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS, complete with 17 evidence files.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`: PASS, complete with 15 evidence files.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS, 280 checks, stdlib structural fallback.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with warning `compact task packet over target: 1887 > 1800`.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.

Post-change validation is recorded after artifact generation and before commit in the final updated version of this file.

Post-change commands run after task artifact writes:

- `git status --short --branch`: PASS, expected task/report/context/index changes present on `main...origin/main`.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task inspect AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task evidence AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: NOT_RUN/unsupported positional form; CLI rejected extra argument.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, 90 tasks and latest task is `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS, global selector still returned `AIDE-APPLY-LIFECYCLE-PLAN-01`; recorded as warning.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: PASS, complete with 16 evidence files and no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS, complete with 17 evidence files and no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS, 280 checks, stdlib structural fallback.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS with warning `compact task packet over target: 1950 > 1800`.
- `py -3 -c <json parse and no-execution proof script>`: PASS, parsed 11 rollback dry-run JSON reports, 3 rollback records, 3 generated plans, and 3 expected reports; verified no enabling execution flags.
- `rg` boundary text search over changed task/report/index/context files: PASS, required concepts are represented as report-only, blocked, deferred, non-goals, schema labels, or prohibited surfaces.
- `rg` enabling-marker search for `rollback_apply_executed": true`, `rollback_execution_implemented": true`, `uninstall_apply_executed": true`, `lifecycle_apply_executed": true`, `scoped_transaction_apply_executed": true`, `target_files_mutated": true`, `production_ready": true`, and `release_ready": true`: PASS, no matches.

Not run:

- `py -3 .aide/scripts/aide_lite.py lifecycle-rollback status`, `dry-run`, or `verify`: NOT_RUN because no `lifecycle-rollback` command was implemented or authorized in this WorkUnit.
- `py -3 -m py_compile .aide/scripts/aide_lite.py`: NOT_RUN because no code changed.
- Focused lifecycle rollback dry-run tests: NOT_RUN because no code or test path was authorized or changed.
