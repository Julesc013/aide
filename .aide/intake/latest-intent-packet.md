# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 4fdfdc67f2a70a86c8beb8fd2548c51731a569c8d738b81b8c2aafe342edee53
- raw_prompt_excerpt: Continue the existing campaign with a bounded correction to task resume-plan: replace unconditional safe_to_resume and historical task references with the existing selected current-task observation, explicit uncertainty and evidence-reus...
- interpreted_goal: Normalize prompt into a bounded github WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- confidence: high
- task_class: github
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

## Repo State Refs

- `.aide/context/latest-context-packet.md`
- `.aide/context/latest-review-packet.md`
- `.aide/context/latest-task-packet.md`
- `.aide/queue/AIDE-WORK-EFFORT-01/status.yaml`
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
