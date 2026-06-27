# Allowed Paths

Writable paths for this check:

- `.aide/queue/AIDE-CHECK-UPDATE-PLAN-V1-01/**`
- `.aide/reports/update-plan-v1-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Read-only source paths inspected:

- `.aide/queue/AIDE-BUILD-UPDATE-PLAN-V1-01/**`
- `.aide/reports/update-plan-v1/**`
- `.aide/protocol/aide-update-plan-v1.schema.json`
- `core/protocol/update_plan.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_update_plan_v1.py`
- `.aide/fixtures/update-plan-v1/**`

Forbidden paths and actions preserved:

- `.aide/release/dist/**`
- `.aide.local/**`
- target repositories
- ScreenSave, Eureka, Dominium
- release tags, uploads, GitHub Releases
- provider/model/network calls
- install/update/migration/repair/rollback/uninstall apply
