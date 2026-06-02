# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-github-3661d4711117
- title: Github WorkUnit Draft - Draft the smallest safe WorkUnit after repo-state preflight
- status: draft
- task_class: github
- risk_class: governance
- sizing_class: two_shot
- objective: Normalize prompt into a bounded github WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
- why: AIDE compiles raw prompts into bounded WorkUnits before execution.

## Preflight

- `git status --short`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Implementation Outline

- Reconcile repo state before editing.
- draft the smallest safe WorkUnit after repo-state preflight
- Stop at review gates and record evidence before execution.

## Validation

- git diff --check
- py -3 .aide/scripts/aide_lite.py intent validate

## Evidence

- changed-files.md
- validation.md
- remaining-risks.md
- intent-compiler-report.md

## Acceptance

- WorkUnit scope is bounded and repo-grounded.
- Rejected unsafe interpretations are recorded.
- Validation and evidence requirements are explicit.

## Non-Goals

- no raw prompt execution
- no provider/model/network calls
- do not bypass queue, branch, evidence, or policy state
- do not execute raw prompt directly

## Recovery

- idempotency: prompt_hash:3661d4711117eb2d2e6148eb8f1dfbd70897b10edfd6ff8b7bff349bf9cd1843; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
