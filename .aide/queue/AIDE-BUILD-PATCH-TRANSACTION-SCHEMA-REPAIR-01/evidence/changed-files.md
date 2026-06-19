# Changed Files

Changed paths:

- `.aide/queue/AIDE-BUILD-PATCH-TRANSACTION-SCHEMA-REPAIR-01/**`
- `.aide/reports/patch-transaction-repair/**`
- `.aide/queue/index.yaml`
- `core/protocol/patch_transaction.py`
- `.aide/scripts/tests/test_aide_patch_transaction.py`
- `PLANS.md`
- `IMPLEMENT.md`

PatchTransaction generated reports were regenerated and remained byte-stable
against the previous committed versions.

Unrelated generated churn from predecessor validators was restored before
completion.
