# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 8a2a93adbe62a35d938abc43f5fd62ce52aabf68676e4a2d16c8c753fc5f72c3
- raw_prompt_excerpt: Add bounded lossless custody of terminal owned AIDE job evidence; preserve full receipt hashes and every log/output byte. Plan source work through AIDE-RETIRED-EVIDENCE-CUSTODY-01. Live raw-copy retirement is separately reviewed; no mode...
- interpreted_goal: Normalize prompt into a bounded evidence WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- confidence: high
- task_class: evidence
- risk_class: high
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

- current_branch:task/aide-current-scoped-lite-qualification-01
- current_role:task
- workflow:trunk_with_dev_integration
- worktree_dirty:true

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
