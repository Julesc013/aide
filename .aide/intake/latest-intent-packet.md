# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 1db3857943cb2185435e9cb4c2c439857ba639fda5ead9a66849fa73f60fdf51
- raw_prompt_excerpt: Repair only the demonstrated installed Lite changelog guard failure with target-owned queue; preserve source admission and original Q31 assertion; qualify actual portable defaults and customization under AIDE-INSTALLED-CHANGELOG-GUARD-01.
- interpreted_goal: Normalize prompt into a bounded install WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: install
- risk_class: governance
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
- `.aide/queue/AIDE-GIT-DEFAULTS-01/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:task/aide-installed-changelog-guard-01
- current_role:task
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
