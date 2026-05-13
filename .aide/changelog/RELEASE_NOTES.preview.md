# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

## Added

- canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles.
- report-only Git workflow detection and branch-role command surface.
- dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards.

## Changed

- WorkUnit recovery preflight now includes branch-role inspection.
- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers.
- Q28 queue state now stops at needs_review with complete evidence.

## Fixed

- made task inspection resolve compact short task ids through the queue index.
- AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run.
