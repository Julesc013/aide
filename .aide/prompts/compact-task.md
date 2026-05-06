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
- `py -3 .aide/scripts/aide_lite.py verify`
- `py -3 .aide/scripts/aide_lite.py review-pack`
- `py -3 .aide/scripts/aide_lite.py ledger scan`
- `py -3 .aide/scripts/aide_lite.py ledger report`
- `py -3 .aide/scripts/aide_lite.py eval run`

## COMMITS

- `<coherent commit sequence>`

## EVIDENCE

- changed files
- validation commands and results
- verifier result and latest verification report path when Q12 verifier is available
- latest review packet path when Q13 review-pack is available
- token estimate, ledger record status, and savings comparison when Q14 ledger behavior is available
- golden task result summary when Q15 eval behavior is available
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
- `VERIFIER_RESULT`
- `REVIEW_PACKET`
- `TOKEN_SURVIVAL_RESULT`
- `TOKEN_LEDGER_RESULT`
- `GOLDEN_TASK_RESULT`
- `RISKS`
- `NEXT`
