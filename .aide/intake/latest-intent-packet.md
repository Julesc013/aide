# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 3661d4711117eb2d2e6148eb8f1dfbd70897b10edfd6ff8b7bff349bf9cd1843
- raw_prompt_excerpt: AIDE-REVIEW-APPLY-00: review and accept the AIDE-APPLY-00 transaction model and AIDE-CHECK-APPLY-00 no-real-apply boundary checkpoint, decide readiness for AIDE-APPLY-01 managed-section patcher, create bounded review-gate queue evidence,...
- interpreted_goal: Normalize prompt into a bounded github WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: github
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
- `.aide/queue/Q17/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:main
- current_role:canonical
- workflow:trunk_without_dev
- worktree_dirty:true

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
