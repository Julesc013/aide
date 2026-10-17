# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: f35e5b47dc7b93ac98480c2398365004b43e4e1337732df9aa4434050e5fbc43
- raw_prompt_excerpt: Preserve unfamiliar outcome ledger metadata and refuse malformed or ambiguous rows before updates, within AIDE-OUTCOME-CONSERVATION-01; qualify existing source and export, then reviewed dev/main integration.
- interpreted_goal: Normalize prompt into a bounded audit WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: audit
- risk_class: low
- sizing_class: audit_only
- safe_to_execute: true
- requires_split: false
- blocked: false
- blocker_reason: none
- next_action: draft the smallest safe WorkUnit after repo-state preflight
- task_execution: false
- provider_or_model_calls: none
- network_calls: none
- raw_long_prompt_storage: false

## Rejected Interpretations

- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly

## Repo State Refs

- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/AIDE-LITE-SUCCESSOR-01/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:dev
- current_role:integration
- workflow:trunk_with_dev_integration
- worktree_dirty:true

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
