# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 8cf2ae77e39511e1e8ee6d4a10746396735eeca00a18764ecb457ed19f15f820
- raw_prompt_excerpt: Prepare AIDE-DAILY-INSTALLED-BINDING-01 under accepted proposal5824d3e. Qualify shipped task identity, selected scope and verification through real installed CLI in owned disposable Git projects. Preserve all17 regression assertions and...
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
- `.aide/queue/AIDE-DAILY-PACK-REFRESH-01/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:task/aide-daily-installed-binding-01
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
