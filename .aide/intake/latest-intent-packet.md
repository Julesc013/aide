# Latest AIDE Intent Packet

- schema_version: aide.intent-packet.v0
- generated_by: aide-lite
- generated_from: inline_prompt
- raw_prompt_hash: 3a5aa29b4b50071703fb1fc5be934bdab1bf4849fdee7967f653350f69ae3add
- raw_prompt_excerpt: AIDE-BUILD-LIFECYCLE-FIXTURE-RUNNER-01: implement a real lifecycle-fixture temp-workspace runner with commands lifecycle-fixture status, lifecycle-fixture run --scenario install-managed-section --mode apply-temp, and lifecycle-fixture ve...
- interpreted_goal: Normalize prompt into a bounded rollback WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- confidence: high
- task_class: rollback
- risk_class: governance
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
- `.aide/queue/AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-AUTHORITY-01/status.yaml`
- `.aide/queue/index.yaml`
- `.aide/repo/file-inventory.json`
- `.aide/repo/latest-repo-intelligence.md`
- `.aide/reports/file-quality-ledger.json`
- `.aide/reports/file-quality-summary.md`

## Branch State Refs

- current_branch:main
- current_role:canonical
- workflow:trunk_without_dev
- worktree_dirty:false

## Validation Hints

- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Evidence Hints

- `changed-files.md`
- `validation.md`
- `remaining-risks.md`
- `intent-compiler-report.md`
