# Allowed Paths

Allowed writes:

- `.aide/protocol/aide-update-receipt-v0.schema.json`
- `core/protocol/update_receipt.py`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_aide_update_receipt_v0.py`
- `.aide/fixtures/update-receipt-v0/**`
- `.aide/reports/update-receipt-v0/**`
- `.aide/queue/AIDE-BUILD-UPDATE-RECEIPT-V0-01/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Forbidden writes preserved:

- target repositories
- `.aide.local/**`
- release archives
- tags, uploads, and GitHub Releases
- DistributionApplyEngine, self-consumer fixture, and canaries
