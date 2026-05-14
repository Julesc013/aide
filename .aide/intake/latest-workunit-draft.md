# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-context-8a0956311647
- title: Context WorkUnit Draft - Inspect latest task/queue state and do not invent product work
- status: draft
- task_class: context
- risk_class: low
- sizing_class: audit_only
- objective: Determine the next safe queue/context action from repo state.
- why: AIDE compiles raw prompts into bounded WorkUnits before execution.

## Preflight

- `git status --short`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Implementation Outline

- Reconcile repo state before editing.
- inspect latest task/queue state and do not invent product work
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
- do not invent product work from vague prompt

## Recovery

- idempotency: prompt_hash:8a0956311647187d73d47ac672d55da73c8feae40cd9fd177414b72e75e0693f; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
