# Drift Review

## Warning Findings

- The older structure note's file counts are stale relative to live
  `repo inventory` and `roots inventory`.
- `.aide/context/latest-task-packet.md` now points at this audit, while
  Reconciler still flags it as stale relative to accepted OKF queue routing.
- OKF current-state pages still point at OKF check routing while queue truth has
  advanced through Reconciler and CapabilityManifest work.
- README still labels Reconciler, CapabilityManifest, ConformanceProfile, and
  PatchTransaction as planned. This is stale relative to some live queue
  evidence but should be normalized in a separate docs-sync task.
- Q37 `task.yaml` says `running`, while live status surfaces say
  `needs_review`.

## Non-Actions

No README, OKF, or historical task metadata repair was performed by this audit.
