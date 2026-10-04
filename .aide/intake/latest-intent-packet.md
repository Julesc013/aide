# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 1ad155f3c8ef4ad2c6291bd9d62484a9da171c2732a89c498ae9bd19aff01288
- raw_prompt_excerpt: Refresh and locally qualify the existing AIDE Lite 1.0.0 candidate with the accepted capability evidence repair. Reuse the current task branch, configured D execution pools and unchanged supervisor; export and build only existing canonic...
- interpreted_goal: Normalize prompt into a bounded release WorkUnit draft: write blocker report and require reviewed authorization before mutation.
- confidence: high
- task_class: release
- risk_class: release
- sizing_class: blocked
- safe_to_execute: false
- requires_split: true
- blocked: true
- blocker_reason: write blocker report and require reviewed authorization before mutation
- next_action: write blocker report and require reviewed authorization before mutation
- task_execution: false
- provider_or_model_calls: none
- network_calls: none
- raw_long_prompt_storage: false

## Rejected Interpretations

- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly
- do not publish releases, tags, or assets from prompt alone

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
- worktree_dirty:false

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py changelog validate`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
