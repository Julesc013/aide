# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-release-23187800b50a
- title: Release WorkUnit Draft - Write blocker report and require reviewed authorization before mutation
- status: draft
- task_class: release
- risk_class: release
- sizing_class: blocked
- objective: Normalize prompt into a bounded release WorkUnit draft: write blocker report and require reviewed authorization before mutation.
- why: AIDE compiles raw prompts into bounded WorkUnits before execution.

## Preflight

- `git status --short`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Implementation Outline

- Reconcile repo state before editing.
- write blocker report and require reviewed authorization before mutation
- Stop at review gates and record evidence before execution.

## Validation

- git diff --check
- py -3 .aide/scripts/aide_lite.py changelog validate
- py -3 .aide/scripts/aide_lite.py intent validate

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
- do not publish releases, tags, or assets from prompt alone

## Recovery

- idempotency: prompt_hash:23187800b50a90d14d4b5adf7f2b97aa15babffb3944f31f6d06cfd4ab0af88c; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
