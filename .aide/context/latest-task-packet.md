# AIDE Latest Task Packet

## PHASE

AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01 - Lifecycle Fixture Temp Runner

## GOAL

Implement one protocol-shaped lifecycle fixture runner slice for `install-managed-section` / `apply-temp`.

## WHY

This is the first narrow implementation slice after the lifecycle fixture proof ladder. It proves temp-only mutation, scoped transaction execution, deterministic verification, rollback-compatible records, path safety, evidence, and honest capability labeling without building a broad kernel scaffold.

## AUTHORITY

The queue task explicitly authorizes implementation:

```yaml
authorizes_implementation: true
implementation_scope: lifecycle-fixture-temp-runner-only
stop_state: needs_review
```

## CONTEXT_REFS

- `.aide/intake/latest-intent-packet.json`
- `.aide/intake/latest-workunit-draft.json`
- `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/`
- `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/`

## ALLOWED_PATHS

- `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/**`
- `.aide/reports/lifecycle-fixture-runner/**`
- `.aide/intake/latest-intent-packet.json`
- `.aide/intake/latest-intent-packet.md`
- `.aide/intake/latest-workunit-draft.json`
- `.aide/intake/latest-workunit-draft.md`
- `.aide/queue/index.yaml`
- `.aide/context/latest-task-packet.md`
- `.aide/reports/task-os-*`
- `core/apply/lifecycle_fixture_runner.py`
- `core/apply/__init__.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_lifecycle_fixture_runner.py`
- `PLANS.md`
- `IMPLEMENT.md`
- `DOCUMENTATION.md`

## REVIEWED_READ_ONLY_PATHS

- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-APPLY-GATE-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01/**`
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/**`
- `.aide/queue/AIDE-CHECK-APPLY-02-RECHECK-01/**`
- `.aide/examples/apply/lifecycle-fixtures/scenarios.json`
- `.aide/examples/apply/lifecycle-fixtures/source-pack/**`
- `.aide/examples/apply/lifecycle-fixtures/generated-plans/install-managed-section.plan.json`
- `.aide/examples/apply/lifecycle-fixtures/expected-reports/install-managed-section.report.json`
- `.aide/examples/apply/lifecycle-fixtures/rollback-records/install-managed-section.rollback.json`
- `.aide/examples/apply/lifecycle-fixtures/target/existing-managed-section/**`
- `.aide/examples/apply/lifecycle-fixtures/expected/install-managed-section/**`

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
- generated lifecycle fixture plans
- expected lifecycle reports
- static canonical fixture target files
- service, Commander, host, provider, or adapter runtime files
- full kernel schema suite

## IMPLEMENTATION

- Keep `.aide/scripts/aide_lite.py` as argument parsing and dispatch only.
- Implement runner behavior in `core/apply/lifecycle_fixture_runner.py`.
- Use minimal seams: `ScenarioLoader`, `TransactionCompiler`, `ScopedExecutor`, `FixtureVerifier`, and `EvidenceReporter`.
- Add only `lifecycle-fixture status`, `run --scenario install-managed-section --mode apply-temp`, and `verify`.
- Mutate only a temp workspace copy of the selected canonical fixture.
- Verify latest completed run by default and fail closed when evidence is missing, malformed, or contradictory.

## EVIDENCE

- `.aide/queue/AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01/evidence/*.md`
- `.aide/reports/lifecycle-fixture-runner/*.json`
- `.aide/reports/lifecycle-fixture-runner/*.md`

## NON_GOALS

No AIDE kernel, service, Commander, provider adapters, branch/worktree automation, full schema suite, OpenTelemetry, SARIF, SPDX, CycloneDX, SLSA, in-toto, OpenAPI, network/model/Gateway calls, release behavior, target repo mutation, canonical fixture mutation, generated plan mutation, expected report mutation, rollback execution, uninstall execution, production-ready claim, or release-ready claim.

## VALIDATION

- targeted lifecycle fixture runner tests
- parser registration test
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture status`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture run --scenario install-managed-section --mode apply-temp`
- `py -3 .aide/scripts/aide_lite.py lifecycle-fixture verify`
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01`
- `git diff --check`

## ACCEPTANCE

- Queue item exists, is indexed, and explicitly authorizes only this implementation.
- Commands exist and are thinly dispatched.
- Runner mutates temp workspace only.
- Path-jail rejection is tested.
- Latest-run verification fails closed on missing or contradictory evidence.
- Reports include `capability_label: fixture_temp_apply_only` and explicit `not_capabilities`.
- Canonical fixtures remain unchanged.
- Task stops at `needs_review` with evidence.

## OUTPUT_SCHEMA

Return a final report with changed files, validation commands/results, evidence refs, capability boundaries, unresolved issues or deferrals, and next task `AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-CHECK-01`.

## TOKEN_ESTIMATE

- approx_tokens: 4500
- budget_status: PASS
