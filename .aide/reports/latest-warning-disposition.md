# Latest Warning Disposition

## AIDE-CHECK-APPLY-01

Current classification is `PASS_WITH_WARNINGS`.

| Class | Count | Disposition |
| --- | ---: | --- |
| harmless | 0 | none |
| expected_generated_state | 5 | generated reports can carry source commit/provenance drift; stale managed-section validation wording was refreshed and rerun validation passed |
| expected_review_gate | 1 | AIDE-APPLY-01 and this checkpoint remain review-gated |
| expected_dirty_pack_provenance | 1 | pack-status may record dirty source before checkpoint commit |
| fixture_only_patch | 1 | fixture patch behavior is intentional and does not authorize active repo apply |
| managed_section_note | 1 | AIDE-APPLY-01 is accepted with notes, not unconditional production apply readiness |
| assigned_next | 1 | next task assigned to AIDE-APPLY-02 |
| blocking | 0 | none |
| unknown_needs_review | 0 | none |

No apply, branch/worktree, target, release, provider/model, network, GitHub API, Gateway, scheduler, install, repair, upgrade, rollback, uninstall, or AIDE-APPLY-02 implementation warning was observed.
