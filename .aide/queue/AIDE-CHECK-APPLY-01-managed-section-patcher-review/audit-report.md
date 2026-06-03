# AIDE-CHECK-APPLY-01 Audit Report

## Executive Verdict

- result: PASS_WITH_WARNINGS
- branch: main
- inspected_commit: a775b1ac7b9a79c3196841e5475b225f2d676743
- worktree_status_at_start: clean
- AIDE-APPLY-01 decision: ACCEPTED_WITH_NOTES
- managed-section readiness: READY_FOR_SCOPED_TRANSACTION_EXECUTOR_WITH_WARNINGS
- AIDE-APPLY-02 readiness: READY_FOR_AIDE_APPLY_02_WITH_WARNINGS
- next_task: AIDE-APPLY-02 - Scoped Transaction Executor v0

## Current AIDE State

- latest_task_before_checkpoint: AIDE-CHECK-APPLY-01 - Managed Section Patcher Review and Apply Boundary Checkpoint
- latest_task_after_checkpoint: AIDE-APPLY-02 - Scoped Transaction Executor v0
- AIDE-APPLY-01 status: needs_review
- transaction model status: report-only and fixture-only transaction model remains review-gated
- managed-section patcher status: fixture-only/report-only patch planning and verification remains review-gated
- no-real-apply boundary: preserved

## AIDE-APPLY-01 Review

- Policies: managed-section marker and ownership policies define explicit marker syntax, generated ownership inside markers, manual ownership outside markers, and blocked conflict classes.
- Schemas: operation, patch, conflict, and report schemas exist and align with fixture-only patch evidence.
- Examples: managed-section examples and fixtures exist for valid, conflict, and report records.
- Core implementation: `core/apply/managed_sections.py` is standard-library-only, narrowly scoped, and does not include branch, GitHub, provider, network, Gateway, target-repo, or broad repo traversal behavior.
- Commands: `managed-section status`, `managed-section validate`, `managed-section fixture-plan`, and `managed-section fixture-verify` exist as report-only or fixture-only commands.
- Fixture patch proof: fixture plans record preimage, postimage, staged-change, and rollback-compatible evidence without active repository patch behavior.
- Manual-content preservation: evidence and tests cover preserving manual prefix/suffix content outside managed markers.
- Conflict detection: missing, duplicate, malformed, nested, binary/unsupported, and hash mismatch cases are blocked or treated as conflicts in policy, code, tests, or evidence.
- Rollback evidence: rollback records are evidence only; no rollback executor is claimed.
- Docs: reference docs describe fixture-safe/report-only status and explicitly defer real apply behavior.
- Tests and golden tasks: core tests, AIDE Lite command tests, and golden tasks cover the managed-section command surface and no-real-apply posture.
- Export pack: portable managed-section support is included; source-generated reports remain source evidence, not target truth.

## No-Real-Apply Boundary

- active repo managed-section apply: no
- active repo transaction apply: no
- install apply: no
- upgrade apply: no
- repair apply: no
- rollback/uninstall apply: no
- branch/worktree apply: no
- merge/push/promotion: no
- release publication: no
- target mutation: no
- provider/model/network: no
- Gateway forwarding: no

## AIDE-APPLY-02 Readiness

AIDE may proceed to planning AIDE-APPLY-02 because AIDE-APPLY-01 provides the required managed-section primitive and evidence posture. The next phase must remain narrower than install/upgrade/repair apply: explicit operator-provided paths, ownership checks, preimage hashes, postimage verification, rollback record creation, and managed-section operations only by default.

## Warnings And Risks

| Class | Count | Disposition |
| --- | ---: | --- |
| harmless | 0 | none |
| expected_generated_state | 5 | generated reports can carry source-commit/provenance drift; stale managed-section validation wording was refreshed and rerun validation passed |
| expected_review_gate | 1 | AIDE-APPLY-01 and this checkpoint remain `needs_review` |
| expected_dirty_pack_provenance | 1 | pack-status may record dirty source while checkpoint artifacts are uncommitted |
| fixture_only_patch | 1 | fixture patching is intentional and does not authorize active repo apply |
| managed_section_note | 1 | AIDE-APPLY-01 is accepted with notes, not unconditional production apply readiness |
| assigned_next | 1 | latest task packet advances to AIDE-APPLY-02 |
| blocking | 0 | none |
| unknown_needs_review | 0 | none |

## Next Plan

Run `AIDE-APPLY-02 - Scoped Transaction Executor v0` as a separate queue item. Do not start install, repair, upgrade, rollback, uninstall, target, branch, release, provider, model, network, Gateway, delete, move, or broad active-repo patching work in that phase.
