# Q15 Golden Task Report

## Summary

Q15 adds deterministic repo-local golden tasks for AIDE's token-saving workflow.
The runner is implemented in `.aide/scripts/aide_lite.py` and exposed as:

- `py -3 .aide/scripts/aide_lite.py eval list`
- `py -3 .aide/scripts/aide_lite.py eval run`
- `py -3 .aide/scripts/aide_lite.py eval run --task TASK_ID`
- `py -3 .aide/scripts/aide_lite.py eval report`

## Catalog

- catalog: `.aide/evals/golden-tasks/catalog.yaml`
- policy: `.aide/policies/evals.yaml`
- runner: `.aide/scripts/aide_lite.py`
- latest JSON report: `.aide/evals/runs/latest-golden-tasks.json`
- latest Markdown report: `.aide/evals/runs/latest-golden-tasks.md`

## Initial Golden Tasks

- `compact-task-packet-required-sections`: checks latest task packet sections, token estimate, and forbidden prompt patterns.
- `context-packet-no-full-repo-dump`: checks latest context packet references repo-map/test-map/context-index and avoids source dumps.
- `verifier-detects-bad-evidence`: checks that malformed evidence fixture is not accepted silently.
- `review-packet-evidence-only`: checks latest review packet evidence refs, verifier refs, decision request, and bounded review shape.
- `token-ledger-budget-check`: checks ledger/report metadata, compact surface records, budget status, and no raw prompt/response storage.
- `adapter-managed-section-determinism`: checks managed AGENTS guidance determinism on an isolated fixture repo.

## Latest Result

- result: PASS
- task_count: 6
- pass_count: 6
- warn_count: 0
- fail_count: 0
- provider_or_model_calls: none
- network_calls: none
- raw_prompt_storage: false
- raw_response_storage: false

## Limitations

These are deterministic local checks for AIDE's token-survival substrate. They
do not prove arbitrary coding task quality, external benchmark performance,
semantic patch correctness, exact tokenizer behavior, provider billing, or model
routing quality.
