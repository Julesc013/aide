# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: cbd052f5deb7b400dd61be92d97a1c0a3e699d5dba7d0c7eacafd4499a1e55dd
- raw_prompt_excerpt: Continue the existing AIDE containment campaign: integrate the already-qualified readonly Windows scoped command host into the normal managed job run entry, pin the existing accepted execution owner, and admit aggregate pool growth under...
- interpreted_goal: Normalize prompt into a bounded evidence WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: evidence
- risk_class: high
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
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
