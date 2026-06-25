# Source Chain Review

The acceptance preserves the complete source chain:

1. `AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`
2. `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-01`
3. `AIDE-BUILD-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`
4. `AIDE-CHECK-DURABLE-LOCAL-WORKER-RUN-SLICE-V0-REPAIR-01`

The original failed check evidence is not rewritten. The repair check reports
`PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, and
routes to this acceptance task.
