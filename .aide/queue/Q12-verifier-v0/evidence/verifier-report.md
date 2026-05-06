# Q12 Verifier Report

## Task

Q12 Verifier v0.

## Objective

Implement deterministic repo-local mechanical verification so future AIDE reviews can use compact verifier/evidence packets instead of long repo or chat-history prompts.

## Scope

Q12 stayed inside verifier policy/templates, AIDE Lite verifier behavior, verifier tests, generated verification/context artifacts, prompt guidance, docs, and Q12 evidence. It did not implement Gateway, providers, model routing, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, LLM-as-judge, automatic repair, exact tokenizer, or token ledger behavior.

## Changed Files

See `.aide/queue/Q12-verifier-v0/evidence/changed-files.md`.

## Validation Commands

Final validation commands are recorded in `.aide/queue/Q12-verifier-v0/evidence/validation.md`.

## Validation Results

The current generated verifier report is `.aide/verification/latest-verification-report.md`.

Final verifier command results:

- `py -3 .aide/scripts/aide_lite.py verify`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --changed-files`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --write-report .aide/verification/latest-verification-report.md`: PASS.
- `py -3 .aide/scripts/aide_lite.py verify --evidence .aide/queue/Q12-verifier-v0/evidence/verifier-report.md`: PASS.

## Generated Artifacts

- `.aide/verification/latest-verification-report.md`: compact structural verification report, 4,178 chars and 1,045 approximate tokens after final regeneration.
- `.aide/context/latest-task-packet.md`: compact Q13 task packet, 3,099 chars and 775 approximate tokens after final regeneration.

## Token Estimates

Verifier output reduces GPT-5.5 review burden by moving these checks local:

- evidence required sections
- task-packet required sections
- file and line-reference resolution
- changed-file path scope
- adapter managed-section drift
- context packet shape
- token budget warnings
- obvious secret-like values

Approximate method: `ceil(chars / 4)`. The verifier report plus Q13 task packet is 7,277 chars and 1,820 approximate tokens after final regeneration.

A naive manual review prompt using `README.md`, `ROADMAP.md`, `AGENTS.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, the Q12 task/prompt, the latest context packet, and the latest task packet is 191,334 chars and 47,834 approximate tokens. That comparison estimates about a 96.2% review-context reduction. This is not exact provider billing; Q14 will formalize durable token ledger comparisons.

## Risks

The verifier is structural and deterministic, not semantic. It does not judge code quality, interpret test logs deeply, prove absence of secrets, or replace independent review.

## Deferrals

Q13 remains responsible for producing review packets. Q14 remains responsible for formal token ledger accounting. Q15 remains responsible for golden-task quality checks.

## Next Recommended Phase

Q13 Evidence Review Workflow, because Q12 now produces compact verifier output that can be fed into evidence-only review.
