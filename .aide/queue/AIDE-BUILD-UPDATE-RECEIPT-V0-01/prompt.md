# Prompt: AIDE-BUILD-UPDATE-RECEIPT-V0-01

Build UpdateReceipt v0 as the next serialized Distribution Safety Wave object.

Repo truth outranks this prompt. Inspect the live checkout, queue index, queue policy, and RollbackBundle acceptance before acting.

Authority:

- Build only.
- Add UpdateReceipt v0 schema/helper/CLI/fixtures/tests/reports/evidence.
- Do not perform update, install, migration, rollback, repair, or uninstall apply.
- Do not mutate target repositories.
- Do not start DistributionApplyEngine, self-consumer fixture, canaries, release archives, tags, uploads, GitHub Releases, provider/model/network calls, runtime surfaces, branch/worktree automation, or source-change apply.

Required output:

- `.aide/protocol/aide-update-receipt-v0.schema.json`
- `core/protocol/update_receipt.py`
- `update-receipt status/project/validate` CLI commands
- `.aide/fixtures/update-receipt-v0/**`
- `.aide/scripts/tests/test_aide_update_receipt_v0.py`
- `.aide/reports/update-receipt-v0/**`
- `.aide/queue/AIDE-BUILD-UPDATE-RECEIPT-V0-01/**`
- updated `.aide/queue/index.yaml`
- updated `PLANS.md` and `IMPLEMENT.md`

Stop at `needs_review` and recommend exactly `AIDE-CHECK-UPDATE-RECEIPT-V0-01`.
