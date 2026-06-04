# Apply Lifecycle Plan

## Status

- task_id: `AIDE-APPLY-LIFECYCLE-PLAN-01`
- status: `needs_review`
- mode: planning-only
- lifecycle_apply_authorized: false
- selected_next_task: `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`

## Lifecycle Planning Gate

The gate passes for planning only:

1. `AIDE-APPLY-02-scoped-transaction-executor-v0` is accepted with notes.
2. `AIDE-CHECK-APPLY-02-RECHECK-01` accepted the repaired executor with notes.
3. Historical `AIDE-CHECK-APPLY-02` remains review history and is superseded by recheck evidence.
4. `AIDE-APPLY-02-REPAIR-01` is accepted with notes.
5. `AIDE-TASK-OS-STATUS-REPAIR-01` repaired stale Task OS latest/current reporting.
6. `task next-plan` selects `AIDE-APPLY-LIFECYCLE-PLAN-01 - Apply Lifecycle Planning`.
7. Repo validation, scoped transaction status, managed-section status, and transaction status pass.
8. No live policy authorizes lifecycle apply execution.

## Capability Reality By Surface

| Surface | Current label | Evidence | Prohibited labels |
| --- | --- | --- | --- |
| install apply | blocked / planned-only | Q43 install model is no-apply; scoped executor policy forbids install apply | implemented, target-capable, production-ready |
| upgrade apply | blocked / planned-only | Q45 upgrade model is no-apply; scoped executor policy forbids upgrade apply | implemented, target-capable, production-ready |
| lifecycle repair apply | blocked / planned-only | Q44 repair model is no-apply; implementation repair is distinct from lifecycle repair apply | implemented, autonomous, production-ready |
| rollback apply | blocked / planned-only | Q46 rollback model is no-apply; rollback records are evidence only | implemented, destructive-capable |
| uninstall apply | blocked / planned-only | Q46 uninstall model is no-apply and preserves unknown/manual content | implemented, destructive-capable |
| fixture lifecycle apply | planned | Scoped executor can apply one explicit managed-section operation in controlled fixture scope; lifecycle schemas/fixtures are not yet defined | active-repo apply, target-repo apply |
| active AIDE repo apply | blocked pending gate | Current tasks allow report/planning and scoped fixture behavior only | broad active-repo apply, production-ready |
| target repo apply | deferred/prohibited pending target authority | Target repos keep target-local truth and require target-local queue authority | source-authorized target mutation |
| branch/worktree mutation | prohibited | AGENTS and queue policy forbid branch/worktree mutation without explicit helper plan | merge/push/promotion capable |
| release/promotion | prohibited | Release publication and promotion are separate reviewed surfaces | release-ready |
| provider/model/Gateway/network support | deferred/prohibited | Scoped executor status reports provider/model/Gateway/network calls none | live-call capable |

## Proof Ladder

1. `AIDE-APPLY-LIFECYCLE-PLAN-01` - report-only lifecycle plan. Authority: this task. Capability after success: planning complete, needs review.
2. `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01` - define lifecycle manifest, plan, report, rollback-record, and fixture repo shape. Authority: queue task. Capability after success: lifecycle schemas and fixtures planned, no apply.
3. `AIDE-LIFECYCLE-ROLLBACK-RECORD-01` - define rollback record compatibility and inversion requirements. Capability after success: rollback evidence contract planned, no rollback execution.
4. `AIDE-LIFECYCLE-FIXTURE-INSTALL-PLAN-01` - create fixture install plan and dry-run evidence. Capability after success: fixture install dry-run, no mutation.
5. `AIDE-LIFECYCLE-FIXTURE-INSTALL-APPLY-01` - only after explicit authorization, execute a single-operation fixture install apply under the scoped executor. Capability after success: fixture-only install apply proof, not active/target apply.
6. `AIDE-LIFECYCLE-FIXTURE-UPGRADE-PLAN-01` - create fixture upgrade plan and dry-run evidence. Capability after success: fixture upgrade dry-run.
7. `AIDE-LIFECYCLE-FIXTURE-UPGRADE-APPLY-01` - only after explicit authorization, execute fixture upgrade apply under scoped single-operation limits. Capability after success: fixture-only upgrade proof.
8. `AIDE-LIFECYCLE-FIXTURE-REPAIR-PLAN-01` - plan repair from explicit drift/defect evidence. Capability after success: fixture repair dry-run.
9. `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-PLAN-01` - validate rollback records and rollback dry-run. Capability after success: rollback dry-run proof.
10. `AIDE-LIFECYCLE-FIXTURE-ROLLBACK-APPLY-01` - only after explicit authorization, execute fixture rollback apply. Capability after success: fixture-only rollback proof.
11. `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-PLAN-01` - plan owned-file and owned-section fixture uninstall with manual content preservation. Capability after success: fixture uninstall dry-run.
12. `AIDE-LIFECYCLE-FIXTURE-UNINSTALL-APPLY-01` - only after explicit authorization, execute fixture uninstall apply. Capability after success: fixture-only uninstall proof.
13. `AIDE-ACTIVE-REPO-APPLY-GATE-01` - define and review active AIDE repo apply authority, dirty-worktree rules, rollback records, and operator approval. Capability after success: active-repo apply gate defined, not executed.
14. `AIDE-TARGET-ADOPTION-GATE-01` - define target-local authority, dry-run adoption, target truth preservation, rollback prerequisites, and review gates. Capability after success: target adoption plan only.
15. `AIDE-RELEASE-POST-LIFECYCLE-GATE-01` - consider release only after fixture, active gate, target dry-run, rollback, and uninstall evidence. Capability after success: release gate planning, not publication.

Every rung has the same default protected paths: `.git/**`, `.github/**`, `.aide.local/**`, secrets, credentials, target-local truth, release publication files, provider/model/Gateway files, branch/worktree automation, manual content outside managed markers, and unknown ownership. Every rung blocks branch/worktree mutation, merge, push, promotion, release publication, GitHub mutation, provider/model calls, Gateway calls, network calls, and broad active-repo apply unless a later reviewed queue task explicitly authorizes a narrower exception.

## Install Plan

Future install apply must require an explicit install manifest, explicit source pack path, explicit fixture or target root, explicit allowed paths, explicit protected paths, generated/managed section boundaries, manual preservation rules, expected preimage hashes for existing files, expected postimages, conflict behavior, dry-run/report mode, rollback-compatible records, evidence, and a review gate. It must start with fixture-only planning and dry-run. It blocks target mutation without target-local authority, overwrites of target truth, broad directory writes, implicit discovery, branch/worktree mutation, provider/model/Gateway/network calls, and release publication.

## Upgrade Plan

Future upgrade apply must require an explicit current installed-state record, desired pack state, diff/transaction plan, allowed paths, protected paths, preimage hashes, postimage verification, manual content preservation, managed-section ownership checks, stale/missing marker behavior, drift detection, rollback-compatible records, dry-run/report mode, fixture-only proof, evidence, and a review gate. It blocks unreviewed active/target mutation, implicit target-truth overwrite, broad apply, and release promotion.

## Lifecycle Repair Plan

Lifecycle repair apply is distinct from `AIDE-APPLY-02-REPAIR-01`, which repaired source implementation findings. Future lifecycle repair apply must require explicit defect/drift evidence, a repair plan, affected paths, allowlist, preimage hashes, postimage verification, manual preservation, rollback-compatible records, dry-run/report mode, fixture proof, evidence, and review. It blocks broad mutation, target mutation without target-local authority, repair without drift evidence, and self-authorized promotion.

## Rollback And Uninstall Plan

Rollback requires rollback record format, rollback compatibility, preimage/postimage inversion, validation before rollback, rollback dry-run, evidence, partial failure behavior, protected path handling, manual content preservation, fixture proof, and review. Uninstall requires an uninstall manifest, owned-file/owned-section distinction, generated-vs-manual boundary, target truth preservation, explicit remove/update operations, evidence, rollback of uninstall where applicable, fixture proof, and review. Both block deleting manual content, broad deletes, target truth deletion, unknown ownership deletion, branch/worktree mutation, and unreviewed target mutation.

## Active AIDE Repo Apply Gate

Active AIDE repo apply is blocked until a future `AIDE-ACTIVE-REPO-APPLY-GATE-01` task defines explicit allowed paths, protected paths, dirty-worktree policy, branch-ahead policy, local commit policy, rollback-compatible record policy, evidence, review, operator approval, and failure recovery. It must preserve no push, no merge, no branch/worktree mutation, no release, no target mutation, and no provider/Gateway/network calls unless future live authority explicitly permits a narrower action.

## Target Repo Adoption Gate

Target adoption is deferred. Target repos keep their own truth: queue, memory, evidence, doctrine, validators, local state, and target-specific records are not replaced by source AIDE state. Adoption starts with report-only inspection, then target-local dry-run, then target-local apply only after target-local queue authority and rollback/uninstall prerequisites. Source AIDE planning cannot mutate target repos.

## Token / Quality Ledger Interlock

Lifecycle apply does not require a token/quality ledger to define schemas or fixtures, but the token quality ledger remains required before strong token/cost-saving or quality-improvement claims. A future `AIDE-TOKEN-QUALITY-LEDGER-01` should record context size, plan size, selected ContextPacket, validation outcomes, review outcomes, rework count, evidence quality, and any authorized estimated or actual token/cost data.

## Safe Next Batch

Selected next task: `AIDE-LIFECYCLE-SCHEMA-AND-FIXTURE-PLAN-01`.

Reason: it is the smallest lifecycle-enabling WorkUnit that does not widen authority. It defines schemas and fixture shape before any fixture apply, active repo apply, target adoption, rollback execution, release, provider/model, Gateway, or network work.
