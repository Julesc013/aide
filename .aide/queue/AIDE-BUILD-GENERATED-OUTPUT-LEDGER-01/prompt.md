# Prompt

Create and process `AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01`.

Use `.aide/queue/index.yaml` as canonical queue truth.

Goal: build a deterministic, report-only generated-output classifier and
ledger for the AIDE repository.

Required boundaries:

- classify only;
- no regeneration;
- no deletion;
- no cleanup;
- no repair;
- no file movement;
- no source rewrites;
- no reference rewrites;
- no OKF regeneration;
- no report migration;
- no runtime/provider/network/GitHub/branch/release/target-repo behavior.

Stop at `needs_review` with `PASS` or `PASS_WITH_WARNINGS`.

Wave continuation after successful build: `AIDE-BUILD-REPORT-INDEX-01`.

Independent check task: `AIDE-CHECK-GENERATED-OUTPUT-LEDGER-01`.
