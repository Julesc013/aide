# AIDE Token Savings Summary

## Method

- approximation: chars / 4, rounded up
- exact_provider_billing: false
- exact_tokenizer: false
- raw_prompt_storage: false
- raw_response_storage: false

## Latest Compact Surfaces

- `.aide/context/latest-task-packet.md`: 3716 chars / 929 approx tokens / within_budget
- `.aide/context/latest-context-packet.md`: 1943 chars / 486 approx tokens / within_budget
- `.aide/context/latest-review-packet.md`: 6658 chars / 1665 approx tokens / within_budget
- `.aide/verification/latest-verification-report.md`: 4621 chars / 1156 approx tokens / within_budget

## Named Baselines

- `root_history_baseline`: 259044 chars / 64761 approx tokens
- `review_baseline`: 28058 chars / 7015 approx tokens
- `repo_context_baseline`: 276866 chars / 69217 approx tokens
- `token_survival_baseline`: 16938 chars / 4235 approx tokens

## Compact-To-Baseline Comparisons

- `.aide/context/latest-task-packet.md` vs `root_history_baseline`: 98.6% estimated reduction (929 vs 64761 approx tokens)
- `.aide/context/latest-review-packet.md` vs `review_baseline`: 76.3% estimated reduction (1665 vs 7015 approx tokens)
- `.aide/context/latest-context-packet.md` vs `repo_context_baseline`: 99.3% estimated reduction (486 vs 69217 approx tokens)

## Largest Ledger Surfaces

- `AGENTS.md` (generated_adapter): 2368 approx tokens
- `.aide/cache/latest-cache-keys.json` (cache_report): 2243 approx tokens
- `.aide/queue/Q18-cache-local-state-boundary/evidence/validation.md` (evidence_packet): 2203 approx tokens
- `.aide/queue/Q17-router-profile-v0/evidence/validation.md` (evidence_packet): 2141 approx tokens
- `.aide/queue/Q16-outcome-controller-v0/evidence/validation.md` (evidence_packet): 1698 approx tokens
- `.aide/context/latest-review-packet.md` (review_packet): 1665 approx tokens
- `.aide/prompts/codex-token-mode.md` (baseline_surface): 1593 approx tokens
- `.aide/queue/Q14-token-ledger-savings-report/evidence/validation.md` (evidence_packet): 1579 approx tokens
- `.aide/queue/Q12-verifier-v0/evidence/validation.md` (evidence_packet): 1486 approx tokens
- `.aide/queue/Q15-golden-tasks-v0/evidence/validation.md` (evidence_packet): 1389 approx tokens

## Budget Warnings

- near budget: cache_report `.aide/cache/latest-cache-keys.json` 2243/2400
- near budget: evidence_packet `.aide/queue/Q17-router-profile-v0/evidence/validation.md` 2141/2400
- near budget: evidence_packet `.aide/queue/Q18-cache-local-state-boundary/evidence/validation.md` 2203/2400

## Regression Warnings

- none

## Uncertainty

These are estimated metadata records only. They do not measure provider billing, exact tokenizer behavior, hidden reasoning tokens, cached-token discounts, or quality outcomes. Q15 golden tasks provide deterministic local quality gates, but they do not prove arbitrary coding-task quality.
