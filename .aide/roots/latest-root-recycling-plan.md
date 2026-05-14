# Root Recycling Plan

- plan_id: q40-root-recycling-no-apply-plan
- status: dry_run
- source_commit: ea62607cd7adb72f47b60dcf9b94fa9c4782aadf
- risk_class: high
- no_apply: true
- file_moves: false
- file_deletes: false
- reference_rewrites: false
- target_repo_mutation: false

## Recommended Sequence

- inventory
- classify
- plan
- review
- future_salvage_map
- future_move_map
- future_alias_plan
- future_apply
- future_validate
- future_retire_exception

## Root Plans

- `.agents`: risk=high status=review_required review_files=19
- `.aide`: risk=high status=mixed review_files=1304
- `.aide.local.example`: risk=high status=review_required review_files=6
- `.codex`: risk=high status=review_required review_files=8
- `bridges`: risk=low status=canonical review_files=8
- `core`: risk=high status=mixed review_files=46
- `docs`: risk=medium status=canonical review_files=28
- `environments`: risk=high status=review_required review_files=17
- `evals`: risk=high status=review_required review_files=21
- `fixtures`: risk=low status=canonical review_files=10
- `governance`: risk=high status=review_required review_files=5
- `hosts`: risk=high status=review_required review_files=68
- `inventory`: risk=low status=canonical review_files=12
- `labs`: risk=high status=review_required review_files=8
- `matrices`: risk=low status=canonical review_files=7
- `packaging`: risk=high status=review_required review_files=17
- `platforms`: risk=high status=review_required review_files=9
- `repo-root`: risk=high status=review_required review_files=11
- `research`: risk=high status=review_required review_files=28
- `scripts`: risk=low status=canonical review_files=8
- `shared`: risk=high status=mixed review_files=32
- `specs`: risk=low status=canonical review_files=23

## Blocked Reasons

- .agents: high
- .aide: high
- .aide.local.example: high
- .codex: high
- core: high
- environments: high
- evals: high
- governance: high
- hosts: high
- labs: high
- packaging: high
- platforms: high
- repo-root: high
- research: high
- shared: high

## Boundary

- Q40 plans only. It does not move roots, delete files, rewrite references, absorb tools, or apply maps.
