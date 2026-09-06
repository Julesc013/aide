# Latest AIDE WorkUnit Draft

- schema_version: aide.workunit-draft.v0
- workunit_id: draft-git-a0507ea93c90
- title: Git WorkUnit Draft - Write blocker report and require reviewed authorization before mutation
- status: draft
- task_class: git
- risk_class: release
- sizing_class: blocked
- objective: Normalize prompt into a bounded git WorkUnit draft: write blocker report and require reviewed authorization before mutation.
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
- py -3 .aide/scripts/aide_lite.py git plan
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
- do not merge, push, promote, or prune without reviewed branch plan

## Recovery

- idempotency: prompt_hash:a0507ea93c900f41565f379a9be72425b8cf23766a72da16c2f786a510e2836d; status:draft; compile_only:true
- recovery: Rerun intent compile from repo state; do not replay raw chat as truth.
