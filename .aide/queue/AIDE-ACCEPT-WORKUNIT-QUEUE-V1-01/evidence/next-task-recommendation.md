# Next Task Recommendation

Recommended next task: `AIDE-BUILD-WORKUNIT-CLI-01`

Seed:

Create and process `AIDE-BUILD-WORKUNIT-CLI-01`. Build the first narrow CLI
surface over the accepted WorkUnit queue object. Keep scope limited to
read/project/inspect-style queue operations first: `workunit status`,
`workunit list`, `workunit inspect`, and `workunit validate` using accepted
WorkUnit Queue V1, EvidencePacket, and contract envelope shapes. Do not
implement claim/run/finish/repair yet unless explicitly authorized by the
WorkUnit and repo policy. Do not build TestJob schema, Test Broker, Service,
Commander, provider adapters, branch/worktree automation, scheduler,
supervisor, target repo apply, active repo apply, rollback execution, release,
promotion, network, Gateway, GitHub mutation, or model/provider calls. End at
`needs_review` with evidence.
