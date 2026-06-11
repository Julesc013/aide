# AIDE-BUILD-CONTRACT-ENVELOPE-01

Create and process `AIDE-BUILD-CONTRACT-ENVELOPE-01`.

Introduce the minimal public protocol envelope used by AIDE queue/report/evidence
objects, based on the lifecycle fixture runner slice. Keep scope narrow: define
`apiVersion` / `kind` / `metadata` / `spec` / `status` shape,
`schema_version` / `protocol_version` fields, compatibility fields, and
validation helpers only where used by existing lifecycle fixture runner reports
or queue WorkUnits.

Do not build full kernel schemas, WorkUnit CLI, Test Broker, Service,
Commander, provider adapters, branch/worktree automation, target repo apply,
rollback execution, release, promotion, network, Gateway, GitHub mutation, or
model/provider calls.

End at `needs_review` with evidence.
