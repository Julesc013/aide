# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: file:.aide/queue/AIDE-SYMBOL-DISCOVERY-01/prompt.md
- raw_prompt_hash: aff48aac1e15dc1eb426e021b6a6592cef26a6f5b9e5398a6c2217bd4c31b091
- raw_prompt_excerpt: Extend AIDE's existing quality discovery with bounded fresh Python symbol evidence: exact definitions, syntax-matched calls/imports and existing recorded owner/test/documentation context. Preserve old behavior, explain uncertainty, quali...
- interpreted_goal: Normalize prompt into a bounded install WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: low
- task_class: install
- risk_class: unknown
- sizing_class: two_shot
- safe_to_execute: false
- requires_split: true
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
- `target-local preflight validation; no source-side target mutation`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
