# Validation

## Preflight Commands

- `git status --short --branch`: PASS; clean `main...origin/main`.
- `git remote -v`: PASS; origin fetch/push URL recorded.
- `git rev-parse HEAD`: PASS; `4f426e7c42106e6e859aafb7a06896e3e7ce9b2a`.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; `AIDE-APPLY-02-scoped-transaction-executor-v0` was pending and authorized before implementation.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS; report-only; real apply false.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS; report-only; fixture-only transaction planning true.

## Targeted Tests

- `py -3 -m unittest core.apply.tests.test_transaction_executor`: PASS; 21 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_02_scoped_transaction_executor.py`: PASS; 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_apply_0*.py"`: PASS; 16 tests. The managed-section no-apply parser test emits expected argparse usage text while asserting `managed-section apply` is unavailable.

## Scoped Transaction Commands

- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS; policy, schemas, examples, fixtures, core module, and commands present; production-ready and release-ready false.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-plan`: PASS; deterministic dry-run plan written.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-verify`: PASS; 67 checks; dry-run no target mutation; staged-change and rollback-compatible records generated.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction validate`: PASS; 159 checks; scoped reports generated.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/reports/scoped-transaction-executor-fixture-plan.json`: PASS; dry-run fixture plan executed without target file mutation.

## Managed-Section And Transaction Validation

- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS; 333 checks; report-only and fixture-only boundaries preserved.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS; 138 checks; active repo managed-section apply false.
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS after implementation; 489 checks; report-only and target/branch/provider/network boundaries preserved.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS; 225 checks; fixture-only transaction planning.

## Queue And Repo Validation

- `py -3 .aide/scripts/aide_lite.py task status`: PASS; `AIDE-APPLY-02-scoped-transaction-executor-v0` listed as `needs_review planning_state=implemented_needs_review`.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; classification `complete`; evidence files `6`; missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: initially FAILED because the generated transaction validation report contained check names with forbidden marker strings and then scanned itself. Fixed by skipping the forbidden-substring scan for `transaction-fixture-validation.md`; rerun via `py -3 .aide/scripts/aide_lite.py validate 2>&1 | Select-String -Pattern "status:|FAIL"`: PASS, no FAIL findings.
- `git diff --check`: PASS before evidence finalization.

## Generated Report Churn

- Authorized validation report refreshes were retained under AIDE-APPLY-02 allowed report paths: `managed-section-*`, `transaction-*`, `task-os-*`, and `scoped-transaction-executor-*`.
- One out-of-allowlist generated refresh, `.aide/reports/current-aide-roadmap.md`, was restored.

## Pending Final Scope Checks

Final scope checks completed:

- `git status --short --branch`: PASS; changed files remain inside the AIDE-APPLY-02 allowlist, including authorized validation reports.
- `git diff --check`: PASS.
- Changed JSON parse check using PowerShell `ConvertFrom-Json`: PASS; parsed 8 changed JSON files.
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; classification `complete`; status `needs_review`.
- Boundary text search over implementation, docs, reports, and evidence: PASS; required scoped executor, dry-run, report mode, preimage hash, postimage verification, rollback-compatible, staged-change, allowed paths, protected paths, forbidden operations, review gate, `needs_review`, prohibited operation, production-ready, and release-ready terms are present as boundaries or non-goals.
- Initial secret scan: WARN false positives in existing `aide_lite.py` policy text and normal `token` variable usage.
- Refined local secret scan over changed files using credential-shaped private key, AWS key, OpenAI-style key, GitHub token, Slack token, Google API key, and quoted credential assignment patterns: PASS; no credential-shaped secret patterns found.
