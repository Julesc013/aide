# Allowed Paths

Writes are limited to:

- `.aide/queue/AIDE-ACCEPT-ROLLBACK-BUNDLE-V0-01/**`
- `.aide/reports/rollback-bundle-v0-acceptance/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Read-only source review includes:

- `.aide/queue/AIDE-BUILD-ROLLBACK-BUNDLE-V0-01/**`
- `.aide/queue/AIDE-CHECK-ROLLBACK-BUNDLE-V0-01/**`
- `.aide/reports/rollback-bundle-v0/**`
- `.aide/reports/rollback-bundle-v0-check/**`
- `.aide/protocol/aide-rollback-bundle-v0.schema.json`
- `core/protocol/rollback_bundle.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_rollback_bundle_v0.py`
- `.aide/fixtures/rollback-bundle-v0/**`

Forbidden:

- RollbackBundle implementation edits.
- UpdateReceipt or DistributionApplyEngine creation.
- Apply behavior.
- Target repository mutation or target scan authority.
- Release archives, tags, uploads, GitHub Releases, provider/model/network calls, canaries, and branch/worktree automation.
