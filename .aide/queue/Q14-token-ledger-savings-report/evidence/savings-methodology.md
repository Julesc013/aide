# Q14 Savings Methodology

## Approximation Method

Q14 uses the repo-local approximation:

```text
approx_tokens = ceil(chars / 4)
```

This matches Q09-Q13 token-survival practice and is intentionally simple enough to run without external dependencies.

## Baseline Definitions

Named baselines live in `.aide/reports/token-baselines.yaml`.

Current baseline families:

- `root_history_baseline`: broad root-doc prompt history that compact task packets should replace.
- `review_baseline`: broad manual review bundle that compact review packets should replace.
- `repo_context_baseline`: broad repo-context bundle that context packets should replace.
- `token_survival_baseline`: compact token-survival surfaces used for local size direction checks.

All baselines are estimates and are composed only from committed repo paths. Missing files are warnings.

## Comparison Formula

Compact-to-baseline reduction is computed as:

```text
(baseline_tokens - compact_tokens) / baseline_tokens * 100
```

If a baseline is missing or empty, the comparison is unavailable rather than fabricated.

## What Q14 Measures

- Characters, lines, and approximate tokens for selected committed surfaces.
- Budget status for known task, context, review, verification, and evidence surfaces.
- Regression warnings when current records grow materially over previous records for the same path.
- Estimated reduction percentages against named naive baselines.

## What Q14 Does Not Measure

- Exact tokenizer output.
- Exact provider billing.
- Hidden reasoning tokens.
- Cached-token discounts.
- Provider-side prompt caching.
- Real API usage.
- Quality preservation outcomes.

Q15 Golden Tasks v0 is required to pair token savings with deterministic quality checks.

## Why This Still Helps

Q14 makes token drift visible before Gateway, routing, exact tokenization, or provider billing exist. Future phases can now show whether they are using compact task/review/context packets and whether those packets are growing beyond configured limits.
