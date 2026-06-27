# Blockers And Deferrals

Blockers: none for the build.

Deferrals:

- Independent check remains required before acceptance.
- Acceptance remains required before UpdateReceipt.
- DistributionApplyEngine remains blocked until RollbackBundle and UpdateReceipt are accepted.
- Fixture-only apply, self-consumer fixture, project canaries, release archives, public readiness, and any real target mutation remain future queue work.
