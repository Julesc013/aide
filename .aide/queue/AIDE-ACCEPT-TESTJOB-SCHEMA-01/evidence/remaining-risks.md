# Remaining Risks

- Full JSON Schema Draft 2020-12 validation remains deferred; current validation is the accepted minimal local subset.
- TestJob is metadata-only; Test Broker runtime, async execution, scheduler, leases, worker execution, Service, Commander, providers, Gateway, network, branch automation, target apply, release, and promotion remain future work.
- `.aide/context/latest-task-packet.md` remains stale relative to live queue truth.
- Generated report commands can refresh out-of-scope reports and must continue to be contained.
- PatchTransaction is deliberately not the next task; ReferenceID must be handled first unless a future reviewed queue item changes the order.
