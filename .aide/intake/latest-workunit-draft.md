# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-rollback-12b7ba87e037
- title: Rollback WorkUnit Draft - Require behavior proof and live-test validation plan before implementation
- status: draft
- task_class: rollback
- risk_class: release
- sizing_class: live_test_gate
- objective: Normalize prompt into a bounded rollback WorkUnit draft: require behavior proof and live-test validation plan before implementation.
- why: AIDE compiles raw prompts into bounded WorkUnits before execution.

## Preflight

- `git status --short`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Implementation Outline

- Reconcile repo state before editing.
- require behavior proof and live-test validation plan before implementation
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

- idempotency: prompt_hash:12b7ba87e037bc8368aabfbfeadb61d37a26d3c9b7f0ee31f356aa2b01fd2468; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
