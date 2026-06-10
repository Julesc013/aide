# AIDE Latest Task Packet

## PHASE

AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01 - Lifecycle Fixture Proof Closure

## GOAL

Consolidate the lifecycle fixture dry-run proof ladder after install, upgrade, repair, rollback, and uninstall checkpointing.

## WHY

The dry-run proof ladder is complete through uninstall checkpointing. Before proposing any fixture apply gate, AIDE needs a single closure record that classifies remaining warnings and decides whether expected-report gaps must be repaired or explicitly waived.

## CONTEXT_REFS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/`
- `.aide/reports/lifecycle-fixture-proof-closure/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01/`
- `.aide/reports/lifecycle-fixture-install-dry-run/`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/`
- `.aide/reports/lifecycle-fixture-repair-dry-run/`
- `.aide/reports/lifecycle-fixture-rollback-dry-run/`
- `.aide/reports/lifecycle-fixture-uninstall-dry-run/`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/`

## ALLOWED_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/**`
- `.aide/reports/lifecycle-fixture-proof-closure/**`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `.aide/reports/lifecycle-schema-*`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UPGRADE-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-REPAIR-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-RECORD-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-ROLLBACK-DRY-RUN-CHECK-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-UNINSTALL-DRY-RUN-CHECK-01/**`
- `.aide/reports/lifecycle-fixture-install-dry-run/**`
- `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`
- `.aide/reports/lifecycle-fixture-repair-dry-run/**`
- `.aide/reports/lifecycle-fixture-rollback-dry-run/**`
- `.aide/reports/lifecycle-fixture-uninstall-dry-run/**`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/**`

## FORBIDDEN_PATHS

- `.git/**`
- `.github/**`
- `.aide.local/**`
- `.env`, `.env.*`
- `secrets/**`, `credentials/**`
- target repositories
- release roots
- provider/model/Gateway files
- branch/worktree automation files
- active lifecycle apply and install/upgrade/repair/rollback/uninstall implementation files
- scoped transaction executor and managed-section implementation files
- generated lifecycle fixture plans
- expected lifecycle reports
- static fixture target files
- `core/**`

## REVIEW

- Verify proof-chain checkpoint presence and accepted-with-notes dispositions.
- Classify all expected-report gaps.
- Confirm capability reality remains no-apply.
- Decide whether to proceed to expected-report gap repair or fixture apply gate planning.
- Stop at `needs_review`.

## IMPLEMENTATION

- Create proof-closure queue artifacts and deterministic closure reports.
- Do not repair expected reports in this WorkUnit.
- Do not propose the fixture apply gate as ready while expected-report gaps remain.
- Select `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01` if gap repair is required.

## EVIDENCE

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/*.md`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-proof-closure/*.json`
- `.aide/reports/lifecycle-fixture-proof-closure/*.md`

## NON_GOALS

No expected-report repair, fixture apply gate authorization, fixture apply execution, rollback execution, uninstall execution, lifecycle apply, scoped transaction fixture apply, fixture target mutation, active repo apply, target repo mutation, branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, broad active-repo apply, production-ready claim, or release-ready claim.

## VALIDATION

- git status/diff checks
- JSON parse of closure reports
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py task next-plan`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-LIFECYCLE-FIXTURE-PROOF-CLOSURE-01`
- `py -3 .aide/scripts/aide_lite.py validate`
- lifecycle-schema status/validate/fixture-verify
- boundary text searches and secret scan
- `py -3 .aide/scripts/aide_lite.py commit check --latest`

## ACCEPTANCE

- Proof closure task exists and is indexed.
- Closure reports exist and parse.
- Expected-report gaps are explicitly classified.
- Next WorkUnit is selected.
- Status ends at `needs_review`.
- No apply-capable operation is authorized or executed.

## OUTPUT_SCHEMA

Return the standard AIDE final report with summary, files, validation, unresolved warnings, and forbidden-operation confirmation.

## TOKEN_ESTIMATE

- approx_tokens: 1900
- budget_status: PASS
