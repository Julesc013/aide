# Validation

Task: `AIDE-CHECK-APPLY-02-RECHECK-01`

## Preflight

- `git status --short --branch`: PASS; initial state `## main...origin/main`, clean.
- `git remote -v`: PASS; `origin` is `https://github.com/Julesc013/aide.git` for fetch and push. No push was performed.
- `git rev-parse HEAD`: PASS; initial HEAD `5314c36cbe2762352b1ddf8fb170d6af4d07b004`.
- `git show --stat --oneline --name-status HEAD`: PASS; repair commit is `5314c36 fix(apply): repair scoped transaction executor checkpoint findings`.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; AIDE-APPLY-02 was `needs_review` / `repaired_needs_review` before recheck.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; complete, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; 6 evidence files.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-APPLY-02`: PASS; complete, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-APPLY-02`: PASS; 8 evidence files.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-REPAIR-01`: PASS; complete, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-REPAIR-01`: PASS; 5 evidence files.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.

## Command Help

- `py -3 .aide/scripts/aide_lite.py scoped-transaction --help`: PASS; commands are `status`, `validate`, `fixture-plan`, `fixture-verify`, `run`.
- `py -3 .aide/scripts/aide_lite.py task --help`: PASS; commands include `inspect`, `status`, `evidence`.
- `py -3 .aide/scripts/aide_lite.py validate --help`: PASS.

## Targeted Tests

- `py -3 -m unittest core.apply.tests.test_transaction_executor`: PASS; 27 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_02_scoped_transaction_executor.py`: PASS; 6 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_apply_0*.py"`: PASS; 17 tests. Expected argparse usage text appears for the intentionally unavailable managed-section `apply` command.

## Scoped Transaction Commands

- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-plan`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-verify`: PASS; 68 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction validate`: PASS; 159 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json`: PASS; `target_files_mutated: false`.

## Managed Section And Transaction Commands

- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS; 333 checks.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS; 138 checks.
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS; 484 checks.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS; 225 checks.

## Repo-Wide Validation

- `py -3 .aide/scripts/aide_lite.py validate`: PASS; exact rerun output began with `status: PASS`.
- The prior repair warning about generated-report self-reference is classified as `FALSE_POSITIVE_OR_STALE_REPORT` for this recheck because the exact command now passes.

## Structural Checks

- `git diff --check`: PASS before recheck writes.
- `git diff --check`: PASS after recheck writes.
- JSON parse check: PASS for `.aide/apply/transaction-executor-report.schema.json`, `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`, `.aide/reports/scoped-transaction-executor-example-report.json`, `.aide/reports/scoped-transaction-executor-example-rollback.json`, `.aide/reports/managed-section-fixture-plan.json`, and `.aide/reports/transaction-fixture-plan.json`.
- YAML parse check with PyYAML: NOT_RUN; PyYAML is unavailable in this Python environment. Queue YAML was still exercised by `task status`, `task inspect`, and `task evidence`.

## Post-Write Queue Checks

- `py -3 .aide/scripts/aide_lite.py task status`: PASS; task count `73`; AIDE-APPLY-02, AIDE-APPLY-02-REPAIR-01, and AIDE-CHECK-APPLY-02-RECHECK-01 all show `planning_state=accepted_with_notes`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-APPLY-02-RECHECK-01`: PASS; classification `complete`, evidence files `7`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-APPLY-02-RECHECK-01`: PASS; seven evidence files listed.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-REPAIR-01`: PASS.

## Boundary Searches

Positive boundary search over changed/reviewed files: PASS for all required terms, including `BLOCKED_RESOLVED_PATH_ESCAPE`, `BLOCKED_MULTI_OPERATION_APPLY_NOT_ATOMIC`, `report_path`, and `rollback_record_path`.

Prohibited/non-goal search over changed/reviewed files: PASS for all required terms, including `install apply`, `upgrade apply`, `repair apply`, `rollback/uninstall apply`, `target repo mutation`, `branch/worktree mutation`, `merge`, `push`, `promotion`, `release publication`, `GitHub mutation`, `provider/model calls`, `Gateway calls`, `network calls`, `broad active-repo apply`, `production-ready`, `release-ready`, `target-repo capable`, `install-capable`, `upgrade-capable`, `repair-apply-capable`, `rollback-capable`, and `autonomous apply`.

## Secret Scan

- Broad secret marker scan: WARN; hits were expected policy/evidence/report marker text such as `secrets/**`, `secret scan`, `token`, and `secret_scan_passed`, not credentials.
- Credential-shaped secret scan: PASS; no candidate secrets found.
