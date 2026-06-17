# Finding Taxonomy Review

Status: `PASS`

Reviewed files:

- `.aide/reports/reconciler/finding-taxonomy.json`
- `.aide/reports/reconciler/finding-taxonomy.md`
- `.aide/reports/reconciler-check/check-report.json`

The taxonomy JSON parses and contains the required first-slice categories:

- `stale_context`
- `acceptance_gate_debt`
- `queue_contradiction`
- `missing_evidence`
- `missing_report`
- `protocol_report_mismatch`
- `protocol_okf_mismatch`
- `reference_mismatch`
- `event_mismatch`
- `capability_overclaim`
- `unsupported_accepted_state`
- `stale_generated_report`
- `source_hash_gap`
- `authority_boundary_risk`
- `dirty_state`

The taxonomy does not imply repair, scheduler, runtime, provider, network, Gateway, GitHub, branch/worktree, target apply, active apply, release, or promotion authority.
