# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-release-d94b3f2c8901
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
- do not mutate target repositories from AIDE source repo
- do not publish releases, tags, or assets from prompt alone

## Recovery

- idempotency: prompt_hash:d94b3f2c8901d2810281abeba25c890373ffebb3fcceccf7f53c33e4912a3f78; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
