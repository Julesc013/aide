# Prompt

Create and process `AIDE-BUILD-ROLLBACK-BUNDLE-V0-01`.

Repo truth outranks this prompt. Build RollbackBundle v0 only after confirming UpdatePlan v1 is accepted with zero material findings and zero missing evidence.

RollbackBundle v0 prepares recovery metadata and artifacts for an accepted UpdatePlan. It does not roll back, apply, mutate targets, scan targets, publish releases, create tags, upload artifacts, call provider/model/network services, start canaries, or begin DistributionApplyEngine.

Required outputs:

- `.aide/protocol/aide-rollback-bundle-v0.schema.json`
- `core/protocol/rollback_bundle.py`
- AIDE Lite commands: `rollback-bundle status`, `rollback-bundle project`, `rollback-bundle validate`
- `.aide/fixtures/rollback-bundle-v0/**`
- `.aide/scripts/tests/test_aide_rollback_bundle_v0.py`
- `.aide/reports/rollback-bundle-v0/**`
- `.aide/queue/AIDE-BUILD-ROLLBACK-BUNDLE-V0-01/**`
- updated `.aide/queue/index.yaml`
- updated `PLANS.md` and `IMPLEMENT.md`

Stop at `needs_review` and recommend exactly `AIDE-CHECK-ROLLBACK-BUNDLE-V0-01`.
