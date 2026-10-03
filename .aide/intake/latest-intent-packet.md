# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 987c2a9316935b7ced20eced9aefed1b8245850f71f3072503c9a989de0bc3ef
- raw_prompt_excerpt: Integrate the independently accepted AIDE-SCOPED-JOB-ENTRY-01 source and exact worker qualification into dev only through the existing checkout and owner campaign delegation. Preserve partial containment, failed read exclusion, unqualifi...
- interpreted_goal: Normalize prompt into a bounded git WorkUnit draft: write blocker report and require reviewed authorization before mutation.
- confidence: high
- task_class: git
- risk_class: destructive
- sizing_class: blocked
- safe_to_execute: false
- requires_split: true
- blocked: true
- blocker_reason: write blocker report and require reviewed authorization before mutation
- next_action: write blocker report and require reviewed authorization before mutation
- task_execution: false
- provider_or_model_calls: none
- network_calls: none
- raw_long_prompt_storage: false

## Rejected Interpretations

- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly
- do not merge, push, promote, or prune without reviewed branch plan
- do not move or delete roots without inventory and salvage map

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

- current_branch:task/aide-session-containment-01
- current_role:task
- workflow:trunk_with_dev_integration
- worktree_dirty:false

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py git plan`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
