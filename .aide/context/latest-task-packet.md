# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-CHECK-01 - Independent No-Apply Checkpoint For Static Lifecycle Fixtures

## GOAL

Independently review and checkpoint `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` without fixture repair, lifecycle apply, scoped transaction fixture apply, target mutation, branch/worktree mutation, release work, GitHub/provider/Gateway/network calls, or broad active-repo apply.

## WHY

`AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01` selected this WorkUnit after static fixture materialization. The checkpoint decides whether fixture metadata, expected reports, rollback-compatible records, hashes, validator interlock, no-apply proof, and capability labels are coherent enough for future dry-run/report-only plan generation.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/`
- `.aide/examples/apply/lifecycle-fixtures/`
- `.aide/examples/apply/lifecycle/`
- `.aide/apply/lifecycle-*.schema.json`
- `.aide/reports/lifecycle-fixtures/`
- `.aide/reports/lifecycle-schema-*`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`
- `.aide/reports/scoped-transaction-executor-*`
- `.aide/reports/managed-section-*`
- `.aide/reports/transaction-*`
- `.aide/reports/current-aide-roadmap.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01/**`
- `.aide/examples/apply/lifecycle-fixtures/**`
- `.aide/reports/lifecycle-fixtures/**`
- `.aide/examples/apply/lifecycle/**`
- `.aide/apply/lifecycle-*.schema.json`

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
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply and install/upgrade/repair/rollback/uninstall implementation files
- scoped transaction executor and managed-section implementation files
- `.aide/install/**`
- `.aide/repair/**`
- `.aide/upgrade/**`
- `.aide/rollback/**`
- `.aide/uninstall/**`
- `.aide/release/**`
- `core/**`

## IMPLEMENTATION

- Create the `AIDE-LIFECYCLE-FIXTURE-CHECK-01` queue scaffold.
- Inspect upstream materialization metadata, evidence, and routing.
- Review fixture index, scenarios, expected states/reports, rollback records, and hashes.
- Confirm lifecycle-schema validator interlock and its physical-fixture limitation.
- Confirm no forbidden apply, mutation, release, GitHub, provider/model, Gateway, network, or broad active-repo action occurred.
- Record checkpoint disposition `ACCEPTED_WITH_NOTES`.
- Stop at `needs_review`.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/checkpoint.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/fixture-review.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/review.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/next-batch.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-CHECK-01/evidence/*.md`

## NON_GOALS

- No fixture repair, lifecycle apply implementation/execution, scoped transaction fixture apply, active repo apply, install/upgrade/repair/rollback/uninstall apply, target repo mutation, branch/worktree mutation, merge, push, promotion, tag, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

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
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-CHECK-01`
- task inspect/evidence for `AIDE-LIFECYCLE-FIXTURE-MATERIALIZE-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema validate`
- `py -3 .aide/scripts/aide_lite.py lifecycle-schema fixture-verify`
- `py -3 .aide/scripts/aide_lite.py scoped-transaction status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- parse changed JSON and YAML files
- fixture parse/hash review
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Checkpoint queue scaffold exists and is indexed.
- Upstream materialization task remains `needs_review`.
- All 13 scenarios are present and coherent.
- Expected reports parse and preserve no-mutation metadata.
- Rollback-compatible records parse and preserve no-execution metadata.
- Referenced fixture hashes match current files.
- Lifecycle-schema status, validate, and fixture-verify commands pass.
- No fixture files are modified.
- No lifecycle apply implementation or execution occurs.
- No forbidden operation is performed.
- Checkpoint disposition is `ACCEPTED_WITH_NOTES`.
- Status ends at `needs_review`.

## OUTPUT_SCHEMA

Return the final response format requested by `AIDE-LIFECYCLE-FIXTURE-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 1680
- budget_status: PASS
