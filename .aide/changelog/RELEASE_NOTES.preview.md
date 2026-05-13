# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

## Added

- dry-run Git helper command surface for local branch planning, landing, promotion, sync, and prune guards.

## Changed

- updated next-phase guidance from Q28 redo to Q29 merge/land/promote helpers.
- Q28 queue state now stops at needs_review with complete evidence.
- safe import now treats portable docs/reference governance docs as target-safe.
- Updated agent guidance for target sync and adapter-generated guidance inputs.

## Fixed

- AIDE Lite selftest fixture now includes Q28 policy files when Q28 golden tasks run.
- excluded AIDE-local Q30 branch-policy artifacts from portable pack truth.
- imported target Git policy no longer fails solely because target-local helper plans have not been generated yet.
- Q31 governance validation no longer rejects target-style repos that do not contain a source export pack.
