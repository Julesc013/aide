# Prompt: AIDE-BUILD-UPDATE-PLAN-V1-01

Build UpdatePlan v1 as the next Distribution Safety Wave object after accepted MigrationRecord v0.

Repo truth outranks this prompt. Preserve the queue boundary and stop at `needs_review`.

Authority:

- Build only.
- Do not accept UpdatePlan v1.
- Do not begin RollbackBundle, UpdateReceipt, DistributionApplyEngine, self-consumer fixture, project canaries, AIDE Lite canary archive, public readiness, release publication, runtime, provider/model/network calls, branch/worktree automation, tag, upload, GitHub Release, or target repository mutation.

Required output:

- `.aide/protocol/aide-update-plan-v1.schema.json`
- `core/protocol/update_plan.py`
- `.aide/scripts/aide_lite.py` commands: `update-plan status`, `update-plan project`, `update-plan validate`
- `.aide/scripts/tests/test_aide_update_plan_v1.py`
- `.aide/fixtures/update-plan-v1/**`
- `.aide/reports/update-plan-v1/**`
- `.aide/queue/AIDE-BUILD-UPDATE-PLAN-V1-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Expected result:

- `PASS_WITH_WARNINGS`
- `material_finding_count: 0`
- `missing_evidence: 0`
- `recommended_next_task: AIDE-CHECK-UPDATE-PLAN-V1-01`
