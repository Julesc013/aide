# Task OS Schema Status

Status: `implemented_for_review`

X-OS-00 adds report-only Task OS v0 schema contracts for:

- WorkUnit
- TaskAttempt
- Blocker
- RepairTask
- Wave
- Checkpoint
- TaskLedger
- BlockerLedger
- CapabilityLedger
- BranchProvenance
- CheckpointLedger

The schemas are portable contract records. They do not create authoritative current-history ledgers and do not implement scheduling, apply behavior, branch mutation, promotion, provider/model calls, network calls, release publication, or target-repo mutation.

Example records live under `.aide/examples/task-os/` and are marked as examples.
