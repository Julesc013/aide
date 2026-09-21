# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-release-1de3e5eff2b9
- title: Release WorkUnit Draft - Block until release gates, tags, and assets are approved
- status: draft
- task_class: release
- risk_class: destructive
- sizing_class: blocked
- objective: Normalize prompt into a bounded release WorkUnit draft: block until release gates, tags, and assets are approved.
- why: AIDE compiles raw prompts into bounded WorkUnits before execution.

## Preflight

- `git status --short`
- `py -3 .aide/scripts/aide_lite.py task inspect`
- `py -3 .aide/scripts/aide_lite.py intent validate`

## Implementation Outline

- Reconcile repo state before editing.
- block until release gates, tags, and assets are approved
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

- idempotency: prompt_hash:1de3e5eff2b91fe5908d362f51f8513cdd73a5d87c97b1244425bccf0261fbad; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
