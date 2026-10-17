# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: fb7ff815d7ec9174b3295816b8d0536e25f1a0dcbd0cdbdadfd8a0abe7c43b1f
- raw_prompt_excerpt: Make frequent validated task commits, dev integration and reviewed main promotion the portable AIDE default. Main hosting protection is optional, dev is usually unprotected, task branches are local and short lived unless sharing, importa...
- interpreted_goal: Normalize prompt into a bounded git WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- confidence: high
- task_class: git
- risk_class: governance
- sizing_class: live_test_gate
- safe_to_execute: false
- requires_split: true
- blocked: false
- blocker_reason: none
- next_action: require behavior proof and live-test validation plan before implementation
- task_execution: false
- provider_or_model_calls: none
- network_calls: none
- raw_long_prompt_storage: false

## Rejected Interpretations

- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly
- do not merge, push, promote, or prune without reviewed branch plan

## Repo State Refs

- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/AIDE-DAILY-CURRENT-VIEW-01/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:task/aide-git-defaults-01
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
