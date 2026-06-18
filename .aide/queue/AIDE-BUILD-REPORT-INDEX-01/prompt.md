# Prompt

Create and process `AIDE-BUILD-REPORT-INDEX-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Goal: build a deterministic report index over existing AIDE reports without
moving, renaming, rewriting, repairing, normalizing, or deleting those reports.

The index is generated, non-canonical, and does not replace queue state,
evidence, protocol, policy, or acceptance records.

The index may consume current GeneratedOutputLedger build outputs as
provisional information only. It must not claim GeneratedOutputLedger is
accepted.

Stop at `needs_review` with `PASS` or `PASS_WITH_WARNINGS`.

Recommended next task: `AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`.

Independent report-index check: `AIDE-CHECK-REPORT-INDEX-01`.
