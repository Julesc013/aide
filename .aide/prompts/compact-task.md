# AIDE Compact Task Packet Template

## PHASE

`<queue id and title>`

## GOAL

`<one observable outcome>`

## WHY

`<why this reduces tokens, preserves quality, or unlocks direct utility>`

## CONTEXT_REFS

- `.aide/memory/project-state.md`
- `.aide/context/repo-snapshot.json`
- `.aide/context/repo-map.json`
- `.aide/context/test-map.json`
- `.aide/context/context-index.json`
- `.aide/context/latest-context-packet.md`
- `<task-specific source refs>`

## ALLOWED_PATHS

- `<explicit allowlist>`

## FORBIDDEN_PATHS

- `.git/**`
- `.env`
- `secrets/**`
- `.aide.local/**`
- `<task-specific denylist>`

## IMPLEMENTATION

- `<bounded deliverable>`

## VALIDATION

- `<exact command>`

## COMMITS

- `<coherent commit sequence>`

## EVIDENCE

- changed files
- validation commands and results
- token estimate
- risks and deferrals

## NON_GOALS

- `<explicit deferred work>`

## ACCEPTANCE

- `<pass/fail criterion>`

## OUTPUT_SCHEMA

Return a compact final report with:

- `STATUS`
- `SUMMARY`
- `COMMITS`
- `CHANGED_FILES`
- `VALIDATION`
- `TOKEN_SURVIVAL_RESULT`
- `RISKS`
- `NEXT`
