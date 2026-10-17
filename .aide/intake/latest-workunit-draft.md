# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-install-e01fb12e6927
- title: Install WorkUnit Draft - Require behavior proof and live-test validation plan before implementation
- status: draft
- task_class: install
- risk_class: high
- sizing_class: live_test_gate
- objective: Normalize prompt into a bounded install WorkUnit draft: require behavior proof and live-test validation plan before implementation.
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

- idempotency: prompt_hash:e01fb12e6927bc96f607aaf6fd411633e2751e45af71c5404fa77a00fd5db4e5; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
