# AIDE Latest Task Packet

## PHASE

Q10 - AIDE Lite hardening

## GOAL

Implement Q10 AIDE Lite hardening

## WHY

Continue Q09 token survival by hardening compact packet generation, validation, deterministic adapter updates, and selftests.

## CONTEXT_REFS

- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`
- `.aide/context/repo-snapshot.json` (present)
- `.aide/prompts/compact-task.md`
- `.aide/queue/Q09-token-survival-core/evidence/`

## ALLOWED_PATHS

- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/**`
- `.aide/policies/**`
- `.aide/prompts/**`
- `.aide/context/**`
- `.aide/memory/**`
- `.aide/queue/Q10-*` or future reviewed Q10 queue path
- `AGENTS.md` managed token-survival section
- root docs only when behavior or documentation links change

## FORBIDDEN_PATHS

- `.git/**`
- `.env`
- `secrets/**`
- `.aide.local/**`
- raw provider credentials, API keys, local caches, raw prompt logs
- Gateway, provider, Runtime, Service, Commander, Mobile, MCP/A2A, host, or app-surface implementation paths

## IMPLEMENTATION

- Harden AIDE Lite command structure and deterministic writes.
- Add drift-aware adapter generation and stronger validation.
- Expand tests/selftests around ignore matching, packet budgets, and adapter determinism.
- Keep stdlib-only behavior and no provider/network calls.

## VALIDATION

- `py -3 .aide/scripts/aide_lite.py doctor`
- `py -3 .aide/scripts/aide_lite.py validate`
- `py -3 .aide/scripts/aide_lite.py selftest`
- `py -3 -m unittest discover -s .aide/scripts/tests -t .`
- `py -3 scripts/aide validate`
- `git diff --check`

## COMMITS

- CLI hardening
- tests/selftests
- generated adapter/context updates
- evidence/docs updates if needed

## EVIDENCE

- changed files
- validation commands and results
- compact packet size and budget status
- unresolved risks and deferrals

## NON_GOALS

- No Gateway
- No provider calls
- No model routing
- No local model setup
- No Runtime, Service, Commander, Mobile, MCP/A2A, or host implementation

## ACCEPTANCE

- AIDE Lite commands pass.
- Adapt can run twice without changing output.
- Pack emits a compact packet under the configured hard limit.
- Validation catches missing required files or sections.
- Evidence records token estimates and remaining risks.

## OUTPUT_SCHEMA

Return a compact final report with `STATUS`, `SUMMARY`, `COMMITS`, `CHANGED_FILES`, `VALIDATION`, `TOKEN_SURVIVAL_RESULT`, `RISKS`, and `NEXT`.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: 2587
- approx_tokens: 647
- formal ledger: deferred to Q14
