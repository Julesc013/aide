# Validation

Task: `AIDE-APPLY-02-REPAIR-01`

## Preflight

- `git status --short --branch`: PASS; initial state was `## main...origin/main`, clean.
- `git rev-parse HEAD`: PASS; initial HEAD was `e1bbccebbe7f1d3c5e2d4e8b6c9f03bf73d349c6`.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; AIDE-APPLY-02 is `needs_review`, AIDE-CHECK-APPLY-02 is `needs_review`, and AIDE-APPLY-02-REPAIR-01 is now present as `needs_review`.

## Targeted Tests

- `py -3 -m unittest core.apply.tests.test_transaction_executor`: PASS; 27 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_02_scoped_transaction_executor.py`: PASS; 6 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_apply_0*.py"`: PASS; 17 tests. The disabled managed-section apply command prints expected argparse usage text.

## Scoped Transaction Validation

- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json`: PASS; checked-in example result is `PASS`, `target_files_mutated: false`.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-plan`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-verify`: PASS; 68 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction validate`: PASS; 159 checks.

## Managed Section And Transaction Validation

- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS.
- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS; 333 checks.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS; 138 checks.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS; 484 checks.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS; 225 checks.

## Queue Evidence Checks

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; 6 evidence files.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-CHECK-APPLY-02`: PASS; classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-CHECK-APPLY-02`: PASS; 8 evidence files.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-REPAIR-01`: PASS; classification `complete`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-REPAIR-01`: PASS; 5 evidence files.

## Structural Checks

- `git diff --check`: PASS.
- JSON parse check for changed JSON reports/schemas/examples: PASS for `.aide/apply/transaction-executor-report.schema.json`, `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`, `.aide/reports/scoped-transaction-executor-example-report.json`, `.aide/reports/scoped-transaction-executor-example-rollback.json`, `.aide/reports/managed-section-fixture-plan.json`, and `.aide/reports/transaction-fixture-plan.json`.
- YAML parse check with PyYAML: NOT_RUN; PyYAML is unavailable in the local Python environment. Queue YAML structure was still exercised by `task status`, `task inspect`, and `task evidence`.

## Boundary Searches

Positive boundary terms over changed files: PASS.

- `scoped transaction executor`: 28
- `dry-run`: 60
- `report mode`: 11
- `preimage hash`: 16
- `postimage verification`: 10
- `rollback-compatible`: 16
- `staged-change`: 33
- `allowed paths`: 10
- `protected paths`: 4
- `forbidden operations`: 3
- `review gate`: 8
- `needs_review`: 86
- `symlink`: 15
- `reparse`: 7
- `resolved path`: 4
- `multi-operation`: 3
- `report_path`: 27

Prohibited-surface terms over changed files: PASS as policy, non-goal, blocked, or review-gated text.

- `install apply`: 29
- `upgrade apply`: 10
- `repair apply`: 12
- `rollback/uninstall apply`: 20
- `target repo mutation`: 9
- `branch/worktree mutation`: 19
- `merge`: 24
- `push`: 18
- `promotion`: 23
- `release publication`: 18
- `GitHub mutation`: 13
- `provider/model calls`: 23
- `Gateway calls`: 15
- `network calls`: 26
- `broad active-repo apply`: 15
- `production-ready`: 10
- `release-ready`: 4

## Secret Scan

- Broad marker scan over changed files: WARN; hits were policy, evidence, test fixture, and `secrets` protected-path text, not credentials.
- Credential-shaped scan over changed files: PASS; no candidate secrets found.

## Repo-Wide Validation Warning

- `py -3 .aide/scripts/aide_lite.py validate`: FAIL. The failure is a generated-report self-reference issue in `.aide/reports/managed-section-fixture-validation.md`: the report can include PASS lines such as `omits forbidden marker ... true`, and the repo-wide validator then treats those explanatory PASS lines as forbidden markers. Dedicated `managed-section fixture-verify` and `transaction fixture-verify` were rerun afterward and restored the fixture reports to their stable fixture-only forms.
- This was not repaired in this task because `AIDE-APPLY-02-REPAIR-01` is bounded to the four AIDE-CHECK-APPLY-02 findings and does not authorize a broader validation-report generator repair.
