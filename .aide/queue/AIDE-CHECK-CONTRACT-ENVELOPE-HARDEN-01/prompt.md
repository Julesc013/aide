# Prompt

Task: `AIDE-CHECK-CONTRACT-ENVELOPE-HARDEN-01`

Independently review `AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` and commit
`5d74bb500100e50a3dab31372d59e9afd24eec01`.

Verify schema runtime loading, minimal schema subset validation execution,
helper/schema alignment, report truth, backward compatibility with lifecycle
fixture reports, additive projections, unknown optional field tolerance,
unknown required capability fail-closed behavior, focused tests, no destructive
migration, no overclaiming, and forbidden operation preservation.

Do not build EvidencePacket schema, WorkUnit schema, WorkUnit CLI, TestJob
schema, Test Broker, Service, Commander, provider adapters, branch/worktree
automation, target repo apply, active repo apply, rollback execution, release,
promotion, network, Gateway, GitHub mutation, or model/provider calls.

End with `PASS`, `PASS_WITH_WARNINGS`, `FAILED_VALIDATION`, `BLOCKED`, or
`PARTIAL`.
