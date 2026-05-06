# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

- `.aide/context/latest-task-packet.md`: 3654 chars / 914 approx tokens / within_budget
- `.aide/context/latest-context-packet.md`: 1935 chars / 484 approx tokens / within_budget
- `.aide/context/latest-review-packet.md`: 6763 chars / 1691 approx tokens / within_budget
- `.aide/verification/latest-verification-report.md`: 3431 chars / 858 approx tokens / within_budget

## Named Baselines

- `root_history_baseline`: 226460 chars / 56615 approx tokens
- `review_baseline`: 26798 chars / 6700 approx tokens
- `repo_context_baseline`: 241937 chars / 60485 approx tokens
- `token_survival_baseline`: 15783 chars / 3946 approx tokens

## Compact-To-Baseline Comparisons

- `.aide/context/latest-task-packet.md` vs `root_history_baseline`: 98.4% estimated reduction (914 vs 56615 approx tokens)
- `.aide/context/latest-review-packet.md` vs `review_baseline`: 74.8% estimated reduction (1691 vs 6700 approx tokens)
- `.aide/context/latest-context-packet.md` vs `repo_context_baseline`: 99.2% estimated reduction (484 vs 60485 approx tokens)

## Largest Ledger Surfaces

- `AGENTS.md` (generated_adapter): 2912 approx tokens
- `.aide/queue/Q17-router-profile-v0/evidence/validation.md` (evidence_packet): 2141 approx tokens
- `.aide/cache/latest-cache-keys.json` (cache_report): 2007 approx tokens
- `.aide/queue/Q16-outcome-controller-v0/evidence/validation.md` (evidence_packet): 1698 approx tokens
- `.aide/context/latest-review-packet.md` (review_packet): 1691 approx tokens
- `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md` (evidence_packet): 1579 approx tokens
- `.aide/queue/Q12-verifier-v0/evidence/validation.md` (evidence_packet): 1486 approx tokens
- `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md` (evidence_packet): 1389 approx tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md` (evidence_packet): 1234 approx tokens
- `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md` (evidence_packet): 1122 approx tokens

## Budget Warnings

- near budget: cache_report `.aide/cache/latest-cache-keys.json` 2007/2400
- near budget: evidence_packet `.aide/queue/Q17-router-profile-v0/evidence/validation.md` 2141/2400

## Regression Warnings

- none

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 golden tasks provide deterministic local quality gates, but they do not prove arbitrary coding-task quality.
