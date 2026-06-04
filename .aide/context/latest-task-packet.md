# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01 - Static Lifecycle Fixture Materialization

## GOAL

Materialize static lifecycle fixture inputs, target baselines, expected states, expected report examples, rollback-compatible record examples, scenario metadata, validation reports, and review-gated evidence for future lifecycle dry-run proof tasks.

## WHY

`AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01` selected this WorkUnit as the smallest safe next step after lifecycle schemas and non-mutating examples validated locally. The lifecycle fixture tree must exist before future dry-run plan generation can compare planned lifecycle behavior against deterministic fixture inputs.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-VALIDATOR-01/`
- `.aide/queue/AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-LIFECYCLE-PLAN-01/`
- `.aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0/`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/`
- `.aide/examples/apply/lifecycle-fixtures/`
- `.aide/examples/apply/lifecycle/`
- `.aide/apply/lifecycle-manifest.schema.json`
- `.aide/apply/lifecycle-plan.schema.json`
- `.aide/apply/lifecycle-report.schema.json`
- `.aide/apply/lifecycle-rollback-record.schema.json`
- `.aide/reports/lifecycle-fixtures/`
- `.aide/reports/lifecycle-schema-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
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
- install/upgrade/repair/rollback/uninstall implementation files
- scoped transaction executor implementation files
- managed-section implementation files
- `.aide/install/**`
- `.aide/repair/**`
- `.aide/upgrade/**`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `.aide/release/**`
- `core/**`

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` queue scaffold.
- Materialize `.aide/examples/apply/lifecycle-fixtures/**` as static checked-in fixture content.
- Create fixture index and scenario metadata.
- Create expected lifecycle report examples with `target_files_mutated: false`.
- Create rollback-compatible record examples with `rollback_execution_implemented: false`.
- Create lifecycle fixture validation reports under `.aide/reports/lifecycle-fixtures/**`.
- Record SHA-256 hashes for static fixture files where reports and rollback records reference preimages or postimages.
- Stop at `needs_review`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/fixture-materialization-plan.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/fixture-inventory.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/fixture-scenarios.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/next-batch.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/changed-files.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/preconditions.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/materialization-summary.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/fixture-validation.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/hash-strategy.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/validation.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/boundary-confirmation.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/remaining-risks.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/evidence/next-task-prompt.md`
- `.aide/examples/apply/lifecycle-fixtures/fixture-index.json`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/reports/lifecycle-fixtures/fixture-materialization-report.md`
- `.aide/reports/lifecycle-fixtures/fixture-validation.md`

## NON_GOALS

- No lifecycle apply implementation or execution.
- No scoped transaction apply against fixture targets.
- No active AIDE repo scoped apply mutation.
- No install apply implementation or execution.
- No upgrade apply implementation or execution.
- No lifecycle repair apply implementation or execution.
- No rollback/uninstall implementation or execution.
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
- `git diff --check`
- `git diff --cached --check`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- parse changed JSON files
- parse changed YAML files
- boundary text searches
- changed-file secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Fixture materialization queue scaffold exists and is indexed.
- Static source-pack files exist.
- Static target baseline files exist.
- Static expected state files exist.
- Static expected reports and rollback-compatible records exist.
- Fixture index and scenario metadata parse as JSON.
- Lifecycle schemas/examples still validate locally.
- No lifecycle apply implementation or execution occurs.
- No forbidden operation is performed.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1760
- budget_status: PASS
