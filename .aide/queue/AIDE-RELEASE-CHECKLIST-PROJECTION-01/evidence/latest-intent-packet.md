# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 4f9eb0d8b88e634515e4b9f2b4dc308448c795399c09d385e1eb237705c3b2d3
- raw_prompt_excerpt: Continue the authorised daily-use campaign with a bounded correction to the existing report-only release checklist: project the current policy manual_review_items into JSON and Markdown, preserve no-publish semantics and historical relea...
- interpreted_goal: Normalize prompt into a bounded release WorkUnit draft: block until release gates, tags, and assets are approved.
- confidence: high
- task_class: release
- risk_class: release
- sizing_class: blocked
- safe_to_execute: false
- requires_split: true
- blocked: true
- blocker_reason: block until release gates, tags, and assets are approved
- next_action: block until release gates, tags, and assets are approved
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
- `py -3 .aide/scripts/aide_lite.py changelog validate`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
