# Validation

Preflight commands run before checkpoint artifact writes:

- `git status --short --branch`: PASS_WITH_NOTES, `## main...origin/main [ahead 1]`; deterministic `task-os-*` report refreshes appeared after status commands.
- `git remote -v`: PASS, origin fetch/push configured.
- `git rev-parse HEAD`: PASS, `859f74cdeedb03718aaac1e5b9fba43747ce2a81`.
- `git show --stat --oneline --name-status HEAD`: PASS, prior commit was `audit(docs): add long-turn operating protocol`.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, latest task before this checkpoint was `AI-LONG-TURN-OPERATING-PROTOCOL-00`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS with known selector lag; selected `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: PASS, complete with 16 evidence files.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.

Post-change validation is recorded after artifact generation and before commit in the final updated version of this file.

Post-change commands run after checkpoint artifact writes:

- `git status --short --branch`: PASS_WITH_EXPECTED_CHANGES, checkpoint queue files, queue index/latest task packet updates, and deterministic report refreshes are present on `main...origin/main [ahead 1]`.
- `git diff --check`: PASS.
- `git diff --cached --check`: PASS.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, 92 tasks and latest task is `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS with known warning; global selector still returned `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`: PASS, complete with 18 evidence files and no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS, complete with 17 evidence files and no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS, 280 checks, stdlib structural fallback.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- PowerShell JSON parse over `.aide/reports/lifecycle-fixture-rollback-dry-run/*.json`: PASS, parsed 11 reports and found no execution/enabling true flags.
- PowerShell JSON parse over rollback-compatible records: PASS, parsed 3 records.
- `rg` enabling-marker search for execution/mutation/readiness true flags: PASS, no matches.
- `rg` boundary text search over checkpoint task and latest task packet: PASS, terms appear only as blocked, deferred, non-goal, prohibited, no-execution, or report-only concepts.
- `rg` secret scan over checkpoint task, queue index, and latest task packet: PASS_WITH_FALSE_POSITIVES; hits were `TOKEN_ESTIMATE` in the latest task packet and the literal scanner pattern in `secret-scan.md`.

Not run:

- `py -3 .aide/scripts/aide_lite.py lifecycle-rollback status`, `dry-run`, or `verify`: NOT_RUN because no lifecycle rollback command was implemented or authorized in this WorkUnit.
- Focused rollback execution tests: NOT_RUN because this checkpoint is review-only and no code changed.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PENDING until after the local commit is created.
