# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-install-aff48aac1e15
- title: Install WorkUnit Draft - Draft the smallest safe WorkUnit after repo-state preflight
- status: draft
- task_class: install
- risk_class: unknown
- sizing_class: two_shot
- objective: Normalize prompt into a bounded install WorkUnit draft: draft the smallest safe WorkUnit after repo-state preflight.
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
- target-local preflight validation; no source-side target mutation

## Evidence

- changed-files.md
- validation.md
- remaining-risks.md
- intent-compiler-report.md
- preflight-or-blocker-report.md

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

- idempotency: prompt_hash:aff48aac1e15dc1eb426e021b6a6592cef26a6f5b9e5398a6c2217bd4c31b091; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
