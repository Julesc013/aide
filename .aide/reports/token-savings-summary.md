# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

- `.aide/context/latest-task-packet.md`: 3486 chars / 872 approx tokens / within_budget
- `.aide/context/latest-context-packet.md`: 1922 chars / 481 approx tokens / within_budget
- `.aide/context/latest-review-packet.md`: 7093 chars / 1774 approx tokens / within_budget
- `.aide/verification/latest-verification-report.md`: 4621 chars / 1156 approx tokens / within_budget

## Named Baselines

- `root_history_baseline`: 218298 chars / 54575 approx tokens
- `review_baseline`: 27807 chars / 6952 approx tokens
- `repo_context_baseline`: 233652 chars / 58413 approx tokens
- `token_survival_baseline`: 17122 chars / 4281 approx tokens

## Compact-To-Baseline Comparisons

- `.aide/context/latest-task-packet.md` vs `root_history_baseline`: 98.4% estimated reduction (872 vs 54575 approx tokens)
- `.aide/context/latest-review-packet.md` vs `review_baseline`: 74.5% estimated reduction (1774 vs 6952 approx tokens)
- `.aide/context/latest-context-packet.md` vs `repo_context_baseline`: 99.2% estimated reduction (481 vs 58413 approx tokens)

## Largest Ledger Surfaces

- `AGENTS.md` (generated_adapter): 2742 approx tokens
- `.aide/queue/Q17-router-profile-v0/evidence/validation.md` (evidence_packet): 2141 approx tokens
- `.aide/context/latest-review-packet.md` (review_packet): 1774 approx tokens
- `.aide/queue/Q16-outcome-controller-v0/evidence/validation.md` (evidence_packet): 1698 approx tokens
- `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md` (evidence_packet): 1579 approx tokens
- `.aide/queue/Q12-verifier-v0/evidence/validation.md` (evidence_packet): 1486 approx tokens
- `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md` (evidence_packet): 1389 approx tokens
- `.aide/queue/Q13-evidence-review-workflow/evidence/validation.md` (evidence_packet): 1234 approx tokens
- `.aide/verification/latest-verification-report.md` (verification_report): 1156 approx tokens
- `.aide/queue/Q10-aide-lite-hardening/evidence/validation.md` (evidence_packet): 1122 approx tokens

## Budget Warnings

- near budget: evidence_packet `.aide/queue/Q17-router-profile-v0/evidence/validation.md` 2141/2400

## Regression Warnings

- none

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 golden tasks provide deterministic local quality gates, but they do not prove arbitrary coding-task quality.
