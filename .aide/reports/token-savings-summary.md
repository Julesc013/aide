# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

- `.aide/context/latest-task-packet.md`: 3211 chars / 803 approx tokens / within_budget
- `.aide/context/latest-context-packet.md`: 1893 chars / 474 approx tokens / within_budget
- `.aide/context/latest-review-packet.md`: 7784 chars / 1946 approx tokens / near_budget
- `.aide/verification/latest-verification-report.md`: 4621 chars / 1156 approx tokens / within_budget

## Named Baselines

- `root_history_baseline`: 196031 chars / 49008 approx tokens
- `review_baseline`: 27503 chars / 6876 approx tokens
- `repo_context_baseline`: 211088 chars / 52772 approx tokens
- `token_survival_baseline`: 17509 chars / 4378 approx tokens

## Compact-To-Baseline Comparisons

- `.aide/context/latest-task-packet.md` vs `root_history_baseline`: 98.4% estimated reduction (803 vs 49008 approx tokens)
- `.aide/context/latest-review-packet.md` vs `review_baseline`: 71.7% estimated reduction (1946 vs 6876 approx tokens)
- `.aide/context/latest-context-packet.md` vs `repo_context_baseline`: 99.1% estimated reduction (474 vs 52772 approx tokens)

## Largest Ledger Surfaces

- `AGENTS.md` (generated_adapter): 2470 approx tokens
- `.aide/context/latest-review-packet.md` (review_packet): 1946 approx tokens
- `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md` (evidence_packet): 1579 approx tokens
- `.aide/queue/Q12-verifier-v0/evidence/validation.md` (evidence_packet): 1486 approx tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md` (evidence_packet): 1234 approx tokens
- `.aide/verification/latest-verification-report.md` (verification_report): 1156 approx tokens
- `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md` (evidence_packet): 1122 approx tokens
- `.aide/queue/Q11-context-compiler-v0/evidence/validation.md` (evidence_packet): 1083 approx tokens
- `.aide/queue/Q09-token-survival-core/evidence/validation.md` (evidence_packet): 984 approx tokens
- `.aide/queue/Q10-aide-lite-hardening/evidence/aide-lite-hardening.md` (evidence_packet): 898 approx tokens

## Budget Warnings

- near budget: review_packet `.aide/context/latest-review-packet.md` 1946/2400

## Regression Warnings

- none

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 must add golden tasks so token reductions can be checked against deterministic quality gates.
