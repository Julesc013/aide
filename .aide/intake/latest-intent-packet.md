# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 24d4b33d1ff55ef958078117c7fc91cc5a428d73e06894a8e0e2b8513c334d01
- raw_prompt_excerpt: Plan Q37 Repo Intelligence Index v0 from the current AIDE repository state
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
- `.aide/queue/Q37/status.yaml`
- `.aide/queue/index.yaml`

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
