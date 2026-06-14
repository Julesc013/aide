# AIDE-BUILD-TESTJOB-SCHEMA-01
# Minimal TestJob Schema Slice

Create and process AIDE-BUILD-TESTJOB-SCHEMA-01.

Use .aide/queue/index.yaml as canonical queue truth.

Build the next public protocol slice after accepted WorkerRun:

- Minimal envelope-backed TestJob schema.
- Helper/projection/validation behavior.
- CLI dispatch for:
  - test-job status
  - test-job project --source accepted-artifacts
  - test-job validate
- Additive projections from accepted validation/check/test evidence.
- Focused tests.
- Evidence and reports.

Scope:

- Schema/data/projection slice only.
- No Test Broker runtime.
- No async execution engine.
- No worker execution.
- No scheduler.
- No leases.
- No Service.
- No Commander.
- No provider adapters.
- No branch/worktree automation.
- No target apply.
- No active apply.
- No rollback execution.
- No release.
- No Gateway/network/GitHub/model/provider calls.

The TestJob object should be able to represent, at minimum:

- command argv
- cwd
- environment policy
- status/result
- startedAt/endedAt metadata, nullable
- exitCode, nullable
- duration, nullable
- timeout policy metadata
- log/artifact references
- validation/test framework metadata
- failure summary
- retry/flake fields as metadata-only placeholders
- evidence packet refs
- explicit non-capabilities

Stop at needs_review with evidence.

Recommended next task after build:
AIDE-CHECK-TESTJOB-SCHEMA-01.
