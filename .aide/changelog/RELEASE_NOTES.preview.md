# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

## Added

- canonical AIDE commit discipline and WorkUnit recovery policy.
- AIDE Lite commit, changelog, and task recovery command surfaces.
- canonical Git workflow policy files for branch roles, promotion gates, sync posture, prune posture, and project profiles.
- report-only Git workflow detection and branch-role command surface.

## Changed

- WorkUnit recovery preflight now includes branch-role inspection.
- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers.

## Fixed

- made task inspection resolve compact short task ids through the queue index.

## Notes

- 6 malformed commits were excluded from release-note grouping.
