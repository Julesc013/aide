# Acceptance Summary

Result: `ACCEPTED_WITH_WARNINGS`.

Accepted capability: `aide_self_consumer_fixture_v0`.

Material findings: `0`.

Missing evidence: `0`.

This accepts only the verified self-consumer fixture/proof surface:

- fixture corpus;
- fresh install proof;
- profile generation proof;
- upgrade from previous version proof;
- same-version idempotence proof;
- target-owned state preservation proof;
- rollback proof;
- uninstall/preserve proof;
- offline operation proof;
- source repo vs installed target distinction;
- DistributionApplyEngine-backed accepted context, UpdatePlan, RollbackBundle, predecessor, UpdateReceipt, refusal, temp-workspace, and canonical fixture preservation boundaries.

It does not accept real target apply, source repo self-apply, project canaries, release readiness, release generation, provider/model/network calls, branch/worktree automation, push, or external repository mutation.
