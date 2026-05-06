# Q15 Quality Preservation Report

## Covered Dimensions

Q15 covers these repo-local quality dimensions:

- required sections in compact task and review packets
- absence of forbidden full-history/full-repo prompt patterns
- context references instead of raw repo dumps
- evidence-packet failure detection through verifier fixtures
- token ledger metadata and budget status
- no raw prompt or response storage in ledger/eval reports
- deterministic managed AGENTS section rendering

## Why This Helps

Q14 measures estimated token size. Q15 checks that smaller artifacts still carry
the structural evidence needed for safe implementation and review. Future
optimization work can use this as a deterministic floor: smaller packets are not
valid improvements if golden tasks fail.

## Not Covered Yet

- arbitrary coding-task correctness
- semantic diff quality
- external benchmarks such as SWE-bench
- LLM-as-judge review
- provider/model routing quality
- exact tokenization or provider billing
- cached/reasoning token accounting

## Q16 Use

Q16 Outcome Controller can consume Q15 PASS/WARN/FAIL results as advisory
quality signals for self-optimization recommendations. Q16 should not mutate
policy or prompts automatically without review-gated evidence.
