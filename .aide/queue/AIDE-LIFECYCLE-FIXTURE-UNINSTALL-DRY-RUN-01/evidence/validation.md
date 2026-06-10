# Validation

# Validation

Commands run after task artifact writes:

- `git diff --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`: PASS, complete with 14 evidence files and no missing evidence.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`: PASS.
- PowerShell JSON parse over `.aide/reports/lifecycle-fixture-uninstall-dry-run/*.json`: PASS, parsed 8 uninstall dry-run JSON reports.
- PowerShell JSON parse over uninstall generated plans and static expected report input: PASS.
- `rg` enabling-marker search for uninstall/lifecycle/scoped-transaction execution or readiness true flags: PASS, no matches.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS, 93 tasks and latest task is `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01`.
- `py -3 .aide/scripts/aide_lite.py task next-plan`: PASS with known warning; global selector still returned `AIDE-APPLY-LIFECYCLE-PLAN-01`.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`: PASS.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`: PASS, 280 checks.
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`: PASS, 298 checks.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `rg` boundary text search over task, report, and latest task packet files: PASS, terms appear only as blocked, deferred, non-goal, prohibited, no-execution, or report-only concepts.
- `rg` secret scan over task, reports, latest task packet, and queue index: PASS_WITH_FALSE_POSITIVE; the only hit was `TOKEN_ESTIMATE` in `.aide/context/latest-task-packet.md`.

Not run:

- `py -3 .aide/scripts/aide_lite.py lifecycle-uninstall status`, `dry-run`, or `verify`: NOT_RUN because no lifecycle uninstall command namespace is implemented or authorized in this WorkUnit.
- Focused uninstall execution tests: NOT_RUN because this WorkUnit is report-only and no code changed.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PENDING until after the local commit is created.
