# Prompt

Build `AIDE-BUILD-EVIDENCE-PACKET-SCHEMA-01`.

Implement only the minimal EvidencePacket schema/projection/validation slice
from accepted lifecycle fixture runner and accepted contract-envelope artifacts.

Authority:

```yaml
authorizes_implementation: true
implementation_scope: minimal-evidence-packet-schema-only
predecessor_acceptance_task: AIDE-ACCEPT-CONTRACT-ENVELOPE-01
predecessor_acceptance_status: ACCEPTED_WITH_WARNINGS
stop_state: needs_review
```

Allowed implementation:

- `core/protocol/evidence_packet.py`
- `.aide/protocol/aide-evidence-packet.schema.json`
- thin `evidence-packet status/project/validate` dispatch in
  `.aide/scripts/aide_lite.py`
- focused tests in `.aide/scripts/tests/test_aide_evidence_packet_schema.py`
- additive reports under `.aide/reports/evidence-packet/`
- task-local queue evidence

Do not build a full evidence engine, EvidenceStore, WorkUnit schema, WorkUnit
CLI, TestJob schema, Test Broker, Service, Commander, provider adapters,
branch/worktree automation, target repo apply, active repo apply, rollback
execution, release, promotion, network, Gateway, GitHub mutation, or
model/provider calls.
