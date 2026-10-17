# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 12b7ba87e037bc8368aabfbfeadb61d37a26d3c9b7f0ee31f356aa2b01fd2468
- raw_prompt_excerpt: Qualify an additive AIDE Lite 1.1.0 candidate from the accepted successor builder and development pack at 4f2c3960. Preserve published 1.0.0 assets, run every original consumer family and all 56 declared CLI forms, and prove actual publi...
- interpreted_goal: Normalize prompt into a bounded rollback WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- confidence: high
- task_class: rollback
- risk_class: release
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
- worktree_dirty:false

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
