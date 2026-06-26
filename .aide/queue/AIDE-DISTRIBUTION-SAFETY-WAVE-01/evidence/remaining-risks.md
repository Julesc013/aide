# Remaining Risks

The wave controller itself has no material findings.

Residual risks intentionally deferred to later queue tasks:

- InstallRecord v0 is not implemented.
- MigrationRecord, UpdatePlan, RollbackBundle, UpdateReceipt, DistributionApplyEngine, self-consumer fixture, canary profiles, archive canary, and public readiness are not implemented.
- Fixture-only apply behavior is not authorized until its own build/check/accept sequence.
- Real target apply, target repo mutation, release publication, tags, uploads, GitHub Releases, provider/model/network calls, runtime, Workbench, Commander, Omnigent, and branch/worktree automation remain non-capabilities.
