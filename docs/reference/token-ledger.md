# Token Ledger

## Purpose

Q14 adds deterministic estimated token accounting so AIDE can measure compact task packets, context packets, review packets, verification reports, evidence packets, prompt templates, generated guidance, and named baseline surfaces without storing raw prompts or raw responses.

The primary outputs are:

```bash
.aide/reports/token-ledger.jsonl
.aide/reports/token-baselines.yaml
.aide/reports/token-savings-summary.md
```

## Approximation

Q14 uses the repo-local estimate:

```text
approx_tokens = ceil(chars / 4)
```

This is not exact provider billing. It does not measure exact tokenizer behavior, reasoning tokens, cached-token discounts, provider-side accounting, or quality outcomes.

## Commands

Run from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py ledger scan
py -3 .aide/scripts/aide_lite.py ledger report
py -3 .aide/scripts/aide_lite.py ledger compare --baseline root_history_baseline --file .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py ledger add --file .aide/context/latest-task-packet.md --surface task_packet --phase Q14-token-ledger-savings-report
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Ledger Records

Ledger records are JSON lines with estimated metadata only:

- run id
- phase
- surface
- repo-relative path
- chars
- lines
- approximate tokens
- method
- budget
- budget status
- notes

The ledger must not store raw prompt bodies, raw response bodies, provider keys, local cache contents, `.aide.local` state, or secret material.

## Baselines

`.aide/reports/token-baselines.yaml` defines named naive baselines such as:

- `root_history_baseline`
- `review_baseline`
- `repo_context_baseline`
- `token_survival_baseline`

Baseline comparison sums the existing files named by the baseline and computes:

```text
(baseline_tokens - compact_tokens) / baseline_tokens * 100
```

Missing baseline files are warnings, not hidden assumptions.

## Budget And Regression Status

Budget status values are:

- `within_budget`
- `near_budget`
- `over_budget`
- `unknown_budget`

Q14 warns on hard-limit overages and on token regressions greater than the configured threshold when previous ledger records exist. Regression warnings are advisory in Q14 unless a hard token budget is exceeded.

## Deferred Work

Q14 does not implement exact tokenization, provider billing integration, reasoning-token accounting, cached-token accounting, golden tasks, Gateway, router/cache behavior, provider calls, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, automatic GPT review, LLM-as-judge behavior, automatic repair, or autonomous loops. Q15 should add deterministic golden tasks so token reductions can be checked against quality-preservation gates.
