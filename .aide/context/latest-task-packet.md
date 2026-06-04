# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01 - Lifecycle Schema Validator

## GOAL

Wire local report-only validation for lifecycle schemas, non-mutating examples, rollback-compatible lifecycle records, and fixture-shape examples before any fixture materialization or lifecycle apply proof.

## WHY

`AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` selected this validator as the next safe WorkUnit. The lifecycle schema layer now needs local, repeatable validation before a future fixture materialization task can safely create fixture files. This task remains validation/report/evidence work only.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/apply/lifecycle-manifest.schema.json`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/apply/lifecycle-report.schema.json`
- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/examples/apply/lifecycle/`
- `docs/reference/apply-lifecycle-schemas.md`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/examples/apply/lifecycle/**`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lifecycle_schema_validator.py`
- `.aide/reports/lifecycle-schema-*.md`
- `.aide/reports/lifecycle-schema-*.json`
- `.aide/reports/task-os-*.md`
- `.aide/reports/task-os-*.json`
- `.aide/reports/scoped-transaction-executor-*.md`
- `.aide/reports/scoped-transaction-executor-*.json`
- `.aide/reports/managed-section-*.md`
- `.aide/reports/managed-section-*.json`
- `.aide/reports/transaction-*.md`
- `.aide/reports/transaction-*.json`
- `.aide/reports/current-aide-roadmap.md`
- `docs/reference/apply-lifecycle-schemas.md`
- `README.md`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`
- `.env.*`
- `secrets/**`
- `credentials/**`
- target repositories
- release publication files
- provider/model/Gateway integration files
- branch/worktree automation files
- active lifecycle apply implementation files
- scoped transaction executor implementation files
- managed-section implementation files
- install/upgrade/repair/rollback/uninstall implementation files
- `.aide/install/**`
- `.aide/repair/**`
- `.aide/upgrade/**`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `.aide/release/**`
- `core/**`
- unrelated docs/reference files
- release roots

## IMPLEMENTATION

- Add `lifecycle-schema` report-only commands to `.aide/scripts/aide_lite.py`.
- Validate lifecycle schemas, examples, fixture shape, non-mutating boundaries, path safety, operation allowlists, rollback-execution prohibition, and capability labels.
- Add targeted tests in `.aide/scripts/tests/test_aide_lifecycle_schema_validator.py`.
- Generate lifecycle-schema validation reports and task-local evidence.
- Select exactly one next WorkUnit without executing it.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/validation-matrix.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/next-batch.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/preconditions.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/validator-summary.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/changed-files.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/validation.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/boundary-confirmation.md`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/evidence/remaining-risks.md`
- `.aide/reports/lifecycle-schema-status.md`
- `.aide/reports/lifecycle-schema-validation.md`
- `.aide/reports/lifecycle-schema-fixture-validation.md`

## NON_GOALS

- No lifecycle apply implementation or execution.
- No fixture target materialization.
- No install apply implementation or execution.
- No upgrade apply implementation or execution.
- No lifecycle repair apply implementation or execution.
- No rollback/uninstall implementation or execution.
- No active AIDE repo apply.
- No target repository mutation.
- No branch/worktree mutation, merge, push, promotion, tag, or release publication.
- No GitHub mutation.
- No provider/model calls.
- No Gateway calls.
- No network calls.
- No broad active-repo apply.
- No production-ready or release-ready claim.

## VALIDATION

- `git status --short --branch`
- `git remote -v`
- `git rev-parse HEAD`
- `git show --stat --oneline --name-status HEAD`
- `git diff --check HEAD^ HEAD`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`
- `py -3 .aide/scripts/tests/test_aide_lifecycle_schema_validator.py`
- `py -3 -m py_compile .aide/scripts/aide_lite.py`
- parse changed JSON and YAML files
- boundary text searches
- changed-file secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Lifecycle schema validator task scaffold exists.
- AIDE Lite `lifecycle-schema` commands exist.
- Lifecycle schema and example validation passes locally.
- Non-mutating, path-boundary, rollback-execution, and capability-label checks are covered by targeted tests.
- Lifecycle-schema reports exist.
- Fixture materialization is deferred.
- Lifecycle apply remains unimplemented and unexecuted.
- Selected next task is `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return `STATUS`, `SUMMARY`, `FILES CHANGED`, `LIVE REPO STATE`, `PRECONDITIONS`, `VALIDATOR DESIGN`, `SCHEMA/EXAMPLE VALIDATION`, `TESTS`, `VALIDATION`, `EVIDENCE`, `BOUNDARY REVIEW`, `WARNINGS`, `UNRESOLVED RISKS`, `FORBIDDEN OPERATIONS PRESERVED`, `SAFE NEXT BATCH`, and `NEXT TASK`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- approx_tokens: 1850
- budget_status: PASS
