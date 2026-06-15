# AIDE-CHECK-TESTJOB-SCHEMA-01
# Independent Check For Minimal TestJob Schema

Create and process AIDE-CHECK-TESTJOB-SCHEMA-01.

Use `.aide/queue/index.yaml` as canonical queue truth.

Independently review `AIDE-BUILD-TESTJOB-SCHEMA-01`.

Scope:

- Check only.
- No implementation except minimal evidence/report generation if queue policy requires it.
- No Test Broker runtime.
- No async test execution.
- No scheduler.
- No leases.
- No supervisor.
- No worker execution.
- No WorkUnit claim/run/finish/repair.
- No Service.
- No Commander.
- No provider adapters.
- No branch/worktree automation.
- No target apply.
- No active apply.
- No rollback execution.
- No release.
- No promotion.
- No Gateway/network/GitHub/model/provider calls.

Verify:

- `.aide/protocol/aide-test-job.schema.json` exists and declares kind `TestJob`.
- Schema uses `apiVersion/kind/metadata/spec/status`.
- Schema includes compatibility metadata.
- Schema includes command/cwd/env policy metadata.
- Schema includes status/result/start/end/exit/duration metadata.
- Schema includes timeout/framework/log/artifact/failure/retry/flake metadata.
- Schema includes evidence packet refs and explicit non-capabilities.
- `core/protocol/test_job.py` implements metadata-only helper/projection/validation.
- `.aide/scripts/aide_lite.py` remains CLI dispatch only for `test-job` commands.
- `test-job status/project/validate` commands work.
- Projections are additive and trace accepted predecessor artifacts.
- Source queue tasks are not mutated by projection.
- Explicit non-capabilities are preserved.
- Unsupported execution behavior fails closed or remains absent.
- Envelope, EvidencePacket, WorkUnit, and WorkerRun compatibility is preserved.
- Reports are truthful and do not overclaim Test Broker, async execution, scheduler, leases, Service, Commander, provider, network, GitHub, model, or runtime capability.
- Focused tests pass.
- Validation evidence exists.
- No secrets are emitted.
- No forbidden operations were introduced.

Expected result:

- PASS
- PASS_WITH_WARNINGS
- FAILED_VALIDATION
- BLOCKED
- PARTIAL

Recommended next task if PASS or PASS_WITH_WARNINGS:

`AIDE-ACCEPT-TESTJOB-SCHEMA-01`

Recommended next task after acceptance:

`AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-01`
