# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

- `.aide/context/latest-task-packet.md`: 3215 chars / 804 approx tokens / within_budget
- `.aide/context/latest-context-packet.md`: 1936 chars / 484 approx tokens / within_budget
- `.aide/context/latest-review-packet.md`: 6096 chars / 1524 approx tokens / within_budget
- `.aide/verification/latest-verification-report.md`: 4621 chars / 1156 approx tokens / within_budget

## Named Baselines

- `root_history_baseline`: 210827 chars / 52707 approx tokens
- `review_baseline`: 27550 chars / 6888 approx tokens
- `repo_context_baseline`: 226186 chars / 56547 approx tokens
- `token_survival_baseline`: 15868 chars / 3967 approx tokens

## Compact-To-Baseline Comparisons

- `.aide/context/latest-task-packet.md` vs `root_history_baseline`: 98.5% estimated reduction (804 vs 52707 approx tokens)
- `.aide/context/latest-review-packet.md` vs `review_baseline`: 77.9% estimated reduction (1524 vs 6888 approx tokens)
- `.aide/context/latest-context-packet.md` vs `repo_context_baseline`: 99.1% estimated reduction (484 vs 56547 approx tokens)

## Largest Ledger Surfaces

- `AGENTS.md` (generated_adapter): 2590 approx tokens
- `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md` (evidence_packet): 1579 approx tokens
- `.aide/context/latest-review-packet.md` (review_packet): 1524 approx tokens
- `.aide/queue/Q12-verifier-v0/evidence/validation.md` (evidence_packet): 1486 approx tokens
- `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md` (evidence_packet): 1389 approx tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md` (evidence_packet): 1234 approx tokens
- `.aide/verification/latest-verification-report.md` (verification_report): 1156 approx tokens
- `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md` (evidence_packet): 1122 approx tokens
- `.aide/queue/Q11-context-compiler-v0/evidence/validation.md` (evidence_packet): 1083 approx tokens
- `.aide/queue/Q09-token-survival-core/evidence/validation.md` (evidence_packet): 984 approx tokens

## Budget Warnings

- none

## Regression Warnings

- none

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 must add golden tasks so token reductions can be checked against deterministic quality gates.
