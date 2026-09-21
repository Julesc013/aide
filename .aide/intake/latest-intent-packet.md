# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 1de3e5eff2b91fe5908d362f51f8513cdd73a5d87c97b1244425bccf0261fbad
- raw_prompt_excerpt: Execute AIDE-CONVERGENCE-AND-DELIVERY-01 as a bounded review-gated campaign: preserve and classify all current dirty work and refs; checkpoint the intended .codex neutralization separately; correct only the artificial future-requirements...
- interpreted_goal: Normalize prompt into a bounded release WorkUnit draft: block until release gates, tags, and assets are approved.
- confidence: high
- task_class: release
- risk_class: destructive
- sizing_class: blocked
- safe_to_execute: false
- requires_split: true
- blocked: true
- blocker_reason: block until release gates, tags, and assets are approved
- next_action: block until release gates, tags, and assets are approved
- task_execution: false
- provider_or_model_calls: none
- network_calls: none
- raw_long_prompt_storage: false

## Rejected Interpretations

- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly
- do not move or delete roots without inventory and salvage map
- do not publish releases, tags, or assets from prompt alone

## Repo State Refs

- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/Q17/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:task/aide-cw-integration-broker-01
- current_role:task
- workflow:trunk_with_dev_integration
- worktree_dirty:true

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py changelog validate`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
