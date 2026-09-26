# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-release-56b70b0a8d18
- title: Release WorkUnit Draft - Write blocker report and require reviewed authorization before mutation
- status: draft
- task_class: release
- risk_class: destructive
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
- do not move or delete roots without inventory and salvage map
- do not publish releases, tags, or assets from prompt alone

## Recovery

- idempotency: prompt_hash:56b70b0a8d18170e7908f0eb8cd57f34d45df02d2b6f63cf96f1d30cc0fb82e4; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
