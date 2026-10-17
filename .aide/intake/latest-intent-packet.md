# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: e01fb12e6927bc96f607aaf6fd411633e2751e45af71c5404fa77a00fd5db4e5
- raw_prompt_excerpt: AIDE-ENGINEERING-REVIEW-01: strengthen the existing portable evidence-review prompt and aide-review skill with scoped reuse, behavior preservation, compatibility and impact review; connect generated review packets to that prompt and repo...
- interpreted_goal: Normalize prompt into a bounded install WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- confidence: high
- task_class: install
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
- `.aide/queue/AIDE-QUALITY-DISCOVERY-01/status.yaml`
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
- `target-local preflight validation; no source-side target mutation`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
- `preflight-or-blocker-report.md`
