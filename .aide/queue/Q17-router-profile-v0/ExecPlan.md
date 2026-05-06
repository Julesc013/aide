# Q17 ExecPlan: Router Profile v0

## Purpose

Q17 implements the first AIDE Router Profile: a deterministic, standard-library,
repo-local advisory layer that reads compact task/context packets and existing
token, verifier, review, golden-task, and outcome signals, then explains what
class of executor is justified before tokens are spent.

## Scope

Allowed work is limited to the Q17 queue packet and evidence, routing policy,
advisory model/provider metadata, route-decision artifacts, AIDE Lite route
commands, router tests, generated context/report refreshes, selected prompt and
memory guidance, root docs, selected reference/roadmap docs, and narrow Harness
touchpoints only if clearly justified.

## Non-Goals

Q17 does not implement Gateway, live model calls, provider APIs, local model
setup, OpenAI/Anthropic-compatible APIs, exact tokenization, provider billing,
automatic GPT review, LLM-as-judge behavior, automatic code repair, prompt or
policy mutation, autonomous loops, Runtime, Service, Commander, UI, Mobile,
MCP/A2A, host/app behavior, semantic cache, vector search, embeddings, or Q18
cache/local-state behavior.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline commands.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS`.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 through Q16 are `needs_review`.
- `py -3 .aide/scripts/aide_lite.py doctor` returned `PASS`.
- `py -3 .aide/scripts/aide_lite.py validate` returned `PASS`.
- AIDE Lite snapshot, index, context, verify, review-pack, ledger, eval, outcome, optimize, estimate, and selftest commands ran before edits; generated metadata artifacts were refreshed.
- `.aide/scripts/tests` discovery with `-t .` has the known hidden `.aide` importability failure.
- Harness tests passed, 24 tests.
- Compatibility tests passed, 5 tests.

## Milestones

- [x] Inspect Q09-Q16 outputs and run baseline validation.
- [x] Create Q17 queue packet and evidence skeleton.
- [x] Add routing policy, provider/model metadata, fallback contracts, schema, and examples.
- [x] Extend AIDE Lite with route list/explain/validate behavior and gate-aware route decisions.
- [x] Add route tests for hard floors, failed gates, unknown tasks, no-model routes, and artifacts.
- [x] Generate latest route decision, Q18 task packet, review/token reports, and routing evidence.
- [x] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE
Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger
scan/report/eval list/run/report/outcome report/optimize suggest/route
list/route validate/route explain/pack/estimate/selftest, AIDE Lite test
discovery, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and
`status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the
first unchecked milestone. Route artifacts can be regenerated with
`py -3 .aide/scripts/aide_lite.py route explain`.

## Review Gate

Q17 must end at `needs_review`. Route decisions are advisory only and must not
execute models, providers, Gateway behavior, or policy mutations.

## Completion Notes

Q17 implemented the advisory routing profile and stopped at review. The final
route decision for the generated Q18 compact packet applies the
`architecture_decision` hard floor and recommends `frontier` with
`human_review` fallback. That route is advisory metadata only.
