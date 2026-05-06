# Q16 ExecPlan: Outcome Controller v0

## Purpose

Q16 implements the first AIDE Outcome Controller: a deterministic,
standard-library, repo-local advisory layer that reads token, verification,
review, context, eval, and validation signals and turns them into bounded
recommendations. It is the safe form of self-improvement: observe, classify,
recommend, and require future queue-gated work to apply changes.

## Scope

Allowed work is limited to the Q16 queue packet and evidence,
`.aide/policies/controller.yaml`, `.aide/controller/**`,
`.aide/scripts/aide_lite.py`, `.aide/scripts/tests/**`, generated
controller/context/review/token/eval report updates, selected prompt and memory
guidance, command catalog metadata, root docs, selected reference/roadmap docs,
and narrow Harness touchpoints only if clearly justified.

## Non-Goals

Q16 does not implement Gateway, live routing, provider calls, local model
setup, OpenAI/Anthropic-compatible APIs, exact tokenization, provider billing,
SWE-bench or external benchmarks, LLM-as-judge behavior, automatic GPT review,
automatic code repair, prompt/policy/route mutation, autonomous loops, Runtime,
Service, Commander, UI, Mobile, MCP/A2A, host/app behavior, or Q17 Router
Profile behavior.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 through Q15 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py snapshot`, `index`, `context`, `review-pack`, `ledger scan`, and `ledger report` ran before edits and refreshed generated metadata artifacts.
- `py -3 .aide/scripts/aide_lite.py verify` returned `WARN` before cache cleanup because baseline tests created transient `__pycache__` directories outside the active task allowlist.
- `py -3 .aide/scripts/aide_lite.py eval run` returned `WARN` after review-packet regeneration: five PASS, one WARN, zero FAIL.
- `py -3 .aide/scripts/aide_lite.py selftest` returned `PASS`.
- `py -3 -m unittest discover -s .aide/scripts/tests -t .` failed with the known hidden `.aide` importability limitation.
- `py -3 -m unittest discover -s core/harness/tests -t .` passed, 24 tests.
- `py -3 -m unittest discover -s core/compat/tests -t .` passed, 5 tests.

## Milestones

- [x] Inspect Q09-Q15 outputs and run baseline validation.
- [x] Create Q16 queue packet and evidence skeleton.
- [ ] Add controller policy, README, failure taxonomy, outcome ledger, report, and recommendation output shape.
- [ ] Extend AIDE Lite with outcome report/add and optimize suggest behavior.
- [ ] Add tests for signal readers, outcome records, recommendations, and selftest integration.
- [ ] Generate latest outcome report, recommendations, Q17 task packet, review packet, and token summary.
- [ ] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE
Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger
scan/report/eval list/run/report/outcome report/optimize suggest/pack/estimate
/selftest, AIDE Lite test discovery, `git diff --check`, and targeted secret
scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and
`status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the
first unchecked milestone. Controller reports can be regenerated with
`py -3 .aide/scripts/aide_lite.py outcome report` and
`py -3 .aide/scripts/aide_lite.py optimize suggest`.

## Review Gate

Q16 must end at `needs_review`. Passing Q16 requires independent review
evidence. Recommendations must remain advisory until a future queue item or
explicit human approval implements them.
