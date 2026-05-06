# Golden Tasks v0

## Purpose

Q15 adds deterministic repo-local golden tasks for AIDE's token-saving workflow.
They check that compact artifacts remain structurally useful while avoiding long
history prompts, full repo dumps, raw prompt storage, and model/provider calls.

Token reduction is valid only when these golden tasks pass.

## Commands

List available tasks:

```powershell
py -3 .aide/scripts/aide_lite.py eval list
```

Run all tasks:

```powershell
py -3 .aide/scripts/aide_lite.py eval run
```

Run one task:

```powershell
py -3 .aide/scripts/aide_lite.py eval run --task compact-task-packet-required-sections
```

Read the latest report:

```powershell
py -3 .aide/scripts/aide_lite.py eval report
```

## Reports

Q15 writes deterministic metadata reports:

- `.aide/evals/runs/latest-golden-tasks.json`
- `.aide/evals/runs/latest-golden-tasks.md`

Reports contain task ids, PASS/WARN/FAIL status, check counts, warnings,
errors, related paths, and notes. They do not store raw prompts or raw
responses.

## Initial Tasks

- `compact-task-packet-required-sections`: checks latest compact task packet sections, forbidden prompt patterns, and token estimate.
- `context-packet-no-full-repo-dump`: checks latest context packet references repo-map/test-map/context-index without raw source dumps.
- `verifier-detects-bad-evidence`: checks that malformed evidence fixtures are detected.
- `review-packet-evidence-only`: checks latest review packet evidence refs and decision request.
- `token-ledger-budget-check`: checks ledger/report metadata, budget status, and no raw prompt/response storage.
- `adapter-managed-section-determinism`: checks managed AGENTS section determinism on an isolated fixture repo.

## What Q15 Proves

Q15 proves that AIDE's token-survival substrate has not regressed on required
local structure: packet sections, refs, evidence shape, verifier detection,
review-packet shape, ledger metadata, and adapter determinism.

Q15 does not prove arbitrary coding-task quality, provider performance,
SWE-bench results, semantic patch correctness, model routing quality, or exact
billing savings.

## Future Use

Future token-saving, prompt, context, verifier, review, ledger, adapter, and eval
changes should run:

```powershell
py -3 .aide/scripts/aide_lite.py eval run
```

If a change makes artifacts smaller but golden tasks fail, the change is not a
valid token-saving improvement.

Q16 Outcome Controller should consume golden-task results as deterministic
signals. Gateway, providers, model routing, exact tokenization, external
benchmarks, LLM-as-judge behavior, and automatic repair remain deferred.
