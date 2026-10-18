# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: file:.aide/queue/AIDE-OFFLINE-RESULT-HANDOFF-01/prompt.md
- raw_prompt_hash: e2a27de7537b2c3cc5376f99c4db6b09bc758a0104968e47fe4d123858944acf
- raw_prompt_excerpt: Extend the existing portable task handoff with bounded offline request/result exchange tied to exact selected source inputs. Preserve old behavior, failed work, customization and independent acceptance; qualify source and installed use,...
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
