# Validation

## Preflight

- `git status --short --branch`: PASS; initial status was clean `## main...origin/main`.
- `git remote -v`: PASS; origin fetch/push URL recorded as `https://github.com/Julesc013/aide.git`.
- `git rev-parse HEAD`: PASS; `6a2f26985436394a92af22d3787381182dfa9dbc`.
- `git show --stat --oneline --name-status HEAD`: PASS; implementation commit changed the AIDE-APPLY-02 allowed paths.
- `git diff --check HEAD^ HEAD`: PASS.
- `py -3 .aide/scripts/aide_lite.py task status`: PASS; AIDE-APPLY-02 status `needs_review`, planning_state `implemented_needs_review`.
- `py -3 .aide/scripts/aide_lite.py managed-section status`: PASS; report-only, real apply false.
- `py -3 .aide/scripts/aide_lite.py transaction status`: PASS; report-only, real apply false.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS; review gate `needs_review`, production-ready false, release-ready false.

## Tests

- `py -3 -m unittest core.apply.tests.test_transaction_executor`: PASS; 21 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_apply_02_scoped_transaction_executor.py`: PASS; 5 tests.
- `py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_apply_0*.py"`: PASS; 16 tests. Expected argparse output is emitted while asserting `managed-section apply` remains unavailable.

## Scoped Transaction Commands

- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-plan`: PASS.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction fixture-verify`: PASS; 68 checks; dry-run no target mutation.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction validate`: PASS; 159 checks.
- `py -3 .aide/scripts/aide_lite.py scoped-transaction run --plan .aide/examples/apply/scoped-transaction-executor.dry-run.example.json`: NEEDS_REPAIR; exit 1 with `BLOCKED_PREIMAGE_HASH_MISMATCH`, `status: BLOCKED`, `target_files_mutated: false`. This failed safely because the checked-in example contains placeholder hashes.

## Managed-Section And Transaction Commands

- `py -3 .aide/scripts/aide_lite.py managed-section validate`: PASS; 333 checks.
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`: PASS; 138 checks.
- `py -3 .aide/scripts/aide_lite.py transaction validate`: PASS; 484 checks.
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`: PASS; 225 checks.

## Queue And Repo Commands

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; classification `complete`, evidence files `6`, missing evidence `0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`: PASS; six evidence files available, no missing evidence.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --latest`: PASS for the AIDE-APPLY-02 implementation commit before checkpoint commit.

## Machine-Readable Checks

- PowerShell `ConvertFrom-Json` over `.aide/apply/scoped-transaction-executor.schema.json`, `.aide/apply/transaction-executor-report.schema.json`, `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json`, `.aide/reports/scoped-transaction-executor-example-report.json`, and `.aide/reports/scoped-transaction-executor-example-rollback.json`: PASS.
- `py -3 -c "import yaml; print('yaml ok')"`: NOT_RUN; PyYAML is not installed in the local Python environment.
- YAML fallback: `py -3 .aide/scripts/aide_lite.py task status` is used as the repo-local queue YAML structural check and passed after the index update.

## Boundary Text Searches

- Positive boundary search over AIDE-APPLY-02, AIDE-CHECK-APPLY-02, implementation, tests, docs, policy, and scoped reports: PASS; required scoped transaction executor, dry-run, report mode, preimage hash, postimage verification, rollback-compatible, staged-change, allowed paths, protected paths, forbidden operations, review gate, and `needs_review` terms were found.
- Prohibited/non-goal search over the same scope: PASS; install apply, upgrade apply, repair apply, rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready, and release-ready terms appear as prohibited, false, none, non-goals, or deferred labels.
- Overclaim search for `fully supported`, `target-capable`, `install-capable`, `upgrade-capable`, `broad apply`, and `autonomous apply`: PASS after manual classification; matches were boundary/prohibited-label text, not capability promotion.

## Secret Scan

- Raw marker scan with `rg -n -i "SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY"` over reviewed/changed files: WARN; expected false positives for `secrets/**` protected-path text and secret-scan documentation.
- Refined credential-shaped scan for private keys, AWS keys, OpenAI-style keys, GitHub tokens, Slack tokens, Google API keys, and quoted credential assignments: PASS; no credential-shaped secrets found.

## Command Adaptations

Live help shows `task inspect` and `task evidence` require `--task-id`; the requested positional form was adapted to:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-APPLY-02-scoped-transaction-executor-v0`

## Generated Report Churn

Generated report refreshes were retained because `AIDE-CHECK-APPLY-02/task.yaml` explicitly allows the affected scoped transaction, managed-section, transaction, task-os, and current roadmap reports.
