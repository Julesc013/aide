# Q14 Token Ledger Report

## Commands Added

Q14 extends `.aide/scripts/aide_lite.py` with:

- `ledger scan`
- `ledger add`
- `ledger report`
- `ledger compare`

The commands use Python standard library only and keep records as estimated metadata. They do not store raw prompt or response bodies.

## Generated Reports

- Ledger policy: `.aide/policies/token-ledger.yaml`
- Named baselines: `.aide/reports/token-baselines.yaml`
- Ledger JSONL: `.aide/reports/token-ledger.jsonl`
- Savings summary: `.aide/reports/token-savings-summary.md`
- Latest compact task packet: `.aide/context/latest-task-packet.md`
- Latest review packet: `.aide/context/latest-review-packet.md`

## Record Model

Each ledger record contains:

- `run_id`
- `phase`
- `surface`
- `path`
- `chars`
- `lines`
- `approx_tokens`
- `method`
- `budget`
- `budget_status`
- `notes`

Records intentionally omit raw prompt text, raw response text, provider keys, and local cache contents.

## Budget Status

Q14 defines and tests:

- `within_budget`
- `near_budget`
- `over_budget`
- `unknown_budget`

Known compact surfaces are checked against `.aide/policies/token-budget.yaml` when a matching budget exists. Unknown surfaces are reported as `unknown_budget` rather than treated as hard failures.

## Regression Warnings

Q14 adds advisory regression warnings based on previous ledger records for the same path and a default threshold of 20 percent. The warnings are intended to catch drift back toward verbose packets; Q14 does not fail solely on a regression unless a hard budget is exceeded.

## Current Summary

Command output is recorded in `validation.md`. The generated `.aide/reports/token-savings-summary.md` contains the latest record count, largest surfaces, compact-to-baseline comparisons, budget warnings, and regression warnings.

Latest observed ledger report:

- ledger records: 41
- latest Q15 task packet: 3,211 chars / 803 approximate tokens / `within_budget`
- latest context packet: 1,893 chars / 474 approximate tokens / `within_budget`
- latest review packet: 7,784 chars / 1,946 approximate tokens / `near_budget`
- latest verification report: 4,621 chars / 1,156 approximate tokens / `within_budget`
- budget warnings: 1 near-budget review packet warning
- regression warnings: 0
- raw prompt storage: false
- raw response storage: false

The review packet is close to its hard limit because Q14 evidence now carries ledger, methodology, and regression details. It remains below the configured limit, and Q15 should watch the review packet size carefully.
