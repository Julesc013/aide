# WorkUnit CLI Acceptance Report

- task_id: AIDE-ACCEPT-WORKUNIT-CLI-01
- status: ACCEPTED_WITH_WARNINGS
- decision: ACCEPTED_WITH_WARNINGS
- reviewed_tasks: AIDE-BUILD-WORKUNIT-CLI-01, AIDE-CHECK-WORKUNIT-CLI-01
- reviewed_commits: 721b3061e00d528b6c59386a1049048fbd9a339e, 84fba6ad644d8e99a15223e70af48d7ffcdc67c2
- predecessor_acceptance: AIDE-ACCEPT-WORKUNIT-QUEUE-V1-01 / 36990be285415b2e2356d5a490c7d9cfca823b47

## Summary

The read-only WorkUnit CLI is accepted with warnings. Direct command validation passed for `workunit status`, `workunit list`, `workunit inspect`, and `workunit validate`; unsupported mutation verbs failed closed; path-safety probes failed closed; representative source queue hashes did not change; predecessor lifecycle, contract-envelope, EvidencePacket, and WorkUnit Queue checks passed; refined overclaiming and secret scans passed.

## Accepted Capability

- minimal_workunit_readonly_cli
- read-only WorkUnit CLI: status, list, inspect, validate
- accepted WorkUnit Queue V1 reuse
- source queue task traceability
- path-safe task id handling
- unsupported mutation commands fail closed
- additive WorkUnit CLI reports

## Explicit Non-Capabilities

- workunit mutation CLI, create, claim, run, block, finish, repair
- full WorkUnit runtime, leases, scheduler, supervisor
- WorkerRun schema, TestJob schema, Test Broker
- Service, Commander, provider adapters
- branch/worktree automation, target apply, active apply, rollback execution
- release, promotion, network, Gateway, GitHub mutation, model/provider calls
- production readiness and release readiness

## Validation

- command suite: PASS (46 commands, 0 failures)
- source queue hash comparison: PASS (0 changed paths)
- report parsing: PASS
- refined overclaiming scan: PASS
- refined secret scan: PASS

## Warnings

- Stale latest-task packet is non-blocking because live `.aide/queue/` was canonical and validated.
- Nested Python launcher diagnostics differ from direct PowerShell `py -3`; direct validation passed.
- Full JSON Schema Draft 2020-12 conformance remains deferred.
- Broad scans had false positives, refined scans passed.

## Recommended Next Task

AIDE-BUILD-WORKUNIT-CLI-MUTATION-01
