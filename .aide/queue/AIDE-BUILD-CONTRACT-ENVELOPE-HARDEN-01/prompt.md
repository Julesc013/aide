# Prompt

Task: AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01

Harden the minimal AIDE contract envelope implementation by wiring
`.aide/protocol/aide-envelope.schema.json` into runtime validation. Keep the
scope to contract-envelope schema/runtime alignment only.

Required authority fields:

```yaml
authorizes_implementation: true
implementation_scope: contract-envelope-schema-runtime-alignment-only
stop_state: needs_review
predecessor_task: AIDE-BUILD-CONTRACT-ENVELOPE-01
predecessor_check_task: AIDE-CHECK-CONTRACT-ENVELOPE-01
predecessor_check_status: PASS_WITH_WARNINGS
known_warning_to_address: schema_file_not_wired_into_runtime_validation
```

Do not build EvidencePacket schema, WorkUnit schema, WorkUnit CLI, TestJob
schema, Test Broker, Service, Commander, provider adapters, branch/worktree
automation, target repo apply, active repo apply, rollback execution, release,
promotion, network, Gateway, GitHub mutation, or model/provider calls.
