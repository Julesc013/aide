# Latest Root Inventory

- generated_by: aide-lite
- source_commit: 14259edf98a680ae3624ef046b33cad619680eca
- source_mode: repo_intelligence_index_plus_tracked_delta
- file_count: 1727
- root_count: 22
- no_apply: true
- file_moves: false
- file_deletes: false
- reference_rewrites: false
- provider_or_model_calls: none
- network_calls: none
- next_phase: Q41 Existing Tool Absorption v0

## Root Status Counts

- canonical: 7
- mixed: 3
- review_required: 12

## Root Risk Counts

- high: 15
- low: 6
- medium: 1

## Roots

- `.agents`: files=19 status=review_required risk=high
- `.aide`: files=1281 status=mixed risk=high
- `.aide.local.example`: files=6 status=review_required risk=high
- `.codex`: files=8 status=review_required risk=high
- `bridges`: files=17 status=canonical risk=low
- `core`: files=46 status=mixed risk=high
- `docs`: files=70 status=canonical risk=medium
- `environments`: files=17 status=review_required risk=high
- `evals`: files=21 status=review_required risk=high
- `fixtures`: files=10 status=canonical risk=low
- `governance`: files=5 status=review_required risk=high
- `hosts`: files=68 status=review_required risk=high
- `inventory`: files=12 status=canonical risk=low
- `labs`: files=8 status=review_required risk=high
- `matrices`: files=7 status=canonical risk=low
- `packaging`: files=17 status=review_required risk=high
- `platforms`: files=9 status=review_required risk=high
- `repo-root`: files=11 status=review_required risk=high
- `research`: files=28 status=review_required risk=high
- `scripts`: files=12 status=canonical risk=low
- `shared`: files=32 status=mixed risk=high
- `specs`: files=23 status=canonical risk=low

## Warnings

- unknown_or_unknown-owner_root_candidates: .agents, .aide, .aide.local.example, .codex, bridges, core, docs, environments, evals, fixtures, governance, hosts
- mixed_root_candidates: .aide, core, shared
- high_risk_root_candidates: .agents, .aide, .aide.local.example, .codex, core, environments, evals, governance, hosts, labs, packaging, platforms
