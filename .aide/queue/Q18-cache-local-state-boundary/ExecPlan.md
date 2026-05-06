# Q18 ExecPlan: Cache And Local State Boundary

## Purpose

Q18 defines where AIDE local runtime state may live and adds deterministic
cache-key metadata tooling. It protects the committed repository from secrets,
raw prompts, raw responses, traces, local caches, and machine-specific state
before any future Gateway/provider/runtime work exists.

## Scope

Allowed work is limited to the Q18 queue packet and evidence, `.gitignore`,
`.aide.local.example/**`, cache and local-state policies, `.aide/cache/**`
metadata reports, AIDE Lite cache commands, cache/local-state tests, generated
Q19 packet and compact report refreshes, selected prompt/memory/catalog updates,
root docs, selected reference/roadmap docs, and narrow Harness touchpoints only
if clearly justified.

## Non-Goals

Q18 does not implement Gateway, live model calls, provider APIs, provider
billing, local model setup, OpenAI/Anthropic-compatible APIs, Commander, UI,
mobile, MCP/A2A, autonomous loops, semantic cache, vector databases, embeddings,
exact tokenization, real API usage accounting, LLM-as-judge behavior,
automatic GPT review, automatic code repair, live prompt/response cache, or Q19
Gateway Skeleton behavior.

## Current Facts Verified Before Editing

- `git status --short` was clean before baseline validation.
- `.gitignore` did not exist before Q18.
- `py -3 scripts/aide validate` returned `PASS_WITH_WARNINGS` with 148 info, 7 warnings, and 0 errors.
- `py -3 scripts/aide doctor` returned `PASS_WITH_WARNINGS` with the same known warnings.
- `py -3 scripts/aide self-check` returned `PASS_WITH_WARNINGS`; Q09 through Q17 remain `needs_review` or review-ready.
- Harness tests passed, 24 tests.
- Compatibility tests passed, 5 tests.
- AIDE Lite doctor, validate, snapshot, index, context, verify, review-pack, ledger scan/report, eval list/run/report, outcome report, optimize suggest, route list/validate/explain, estimate, and selftest ran before edits.
- Baseline AIDE Lite validate had one known near-budget token-ledger warning for Q17 validation evidence.
- Baseline direct `.aide/scripts/tests` discovery with `-t .` still fails because hidden `.aide` start directories are not importable by Python unittest.

## Milestones

- [x] Inspect Q09-Q17 outputs and run baseline validation.
- [x] Create Q18 queue packet and evidence skeleton.
- [ ] Add `.gitignore`, `.aide.local.example/**`, cache/local-state policies, and cache metadata directory.
- [ ] Extend AIDE Lite with cache init/status/key/report behavior.
- [ ] Add cache/local-state unit tests.
- [ ] Generate latest cache key reports, Q19 task packet, route/review/token artifacts, and Q18 evidence.
- [ ] Update docs/evidence, run final validation, and stop at review.

## Validation Plan

Run Harness validate/doctor/self-check, Harness and Compatibility tests, AIDE
Lite doctor/validate/snapshot/index/context/verify/review-pack/ledger
scan/report/eval list/run/report/outcome report/optimize suggest/route
list/route validate/route explain/cache init/cache status/cache key/cache
report/pack/estimate/selftest, cache unit tests, `git check-ignore
.aide.local/`, `git diff --check`, and targeted secret scan.

## Recovery

If interrupted, rerun `git status --short`, read this ExecPlan and
`status.yaml`, inspect `.aide/scripts/aide_lite.py`, and continue from the
first unchecked milestone. Cache artifacts can be regenerated with
`py -3 .aide/scripts/aide_lite.py cache report` after Q18 cache commands exist.

## Review Gate

Q18 must end at `needs_review`. Cache keys are metadata only and must not bypass
verifier, golden tasks, route hard floors, or review gates.
