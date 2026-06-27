# Prompt: AIDE-CHECK-INSTALL-RECORD-V0-01

Create and process `AIDE-CHECK-INSTALL-RECORD-V0-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

Authority:

- Check only.
- Do not repair InstallRecord implementation.
- Do not accept InstallRecord v0.
- Do not start MigrationRecord, UpdatePlan, RollbackBundle, UpdateReceipt, DistributionApplyEngine, self-consumer fixtures, project canaries, release publication, provider/model/network calls, branch/worktree automation, or target repo mutation.

Check objectives:

1. Verify `AIDE-BUILD-INSTALL-RECORD-V0-01` exists, is complete, and stopped at `needs_review`.
2. Verify all required task-local evidence exists and `missing_evidence` is `0`.
3. Verify the InstallRecord v0 schema/helper/CLI/fixtures/tests/reports directly model the required no-apply install record contract.
4. Verify fail-closed behavior for missing distribution, missing lock, missing ownership ledger, predecessor mismatch, unknown installed refs, apply authority claims, target mutation claims, unknown required features, absolute paths, traversal paths, source latest output misuse, source output as target truth, and missing evidence.
5. Verify unknown optional features/extensions are tolerated.
6. Verify explicit non-capabilities remain intact.
7. Recommend exactly `AIDE-ACCEPT-INSTALL-RECORD-V0-01` if the check passes.
