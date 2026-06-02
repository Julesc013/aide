# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 4ea75f13756367b28c2748ac36313aa1dbcc2b1425a17efdb34efcac37caf87a
- raw_prompt_excerpt: Create AIDE-CHECK-APPLY-00 as a bounded review checkpoint for AIDE-APPLY-00 transaction model, no-real-apply boundary, schemas, examples, docs, commands, evidence, validation, and export-pack inclusion. Do not implement managed-section p...
- interpreted_goal: Normalize prompt into a bounded docs WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: docs
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
