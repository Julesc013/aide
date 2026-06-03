# Warning Disposition

| Class | Count | Disposition |
| --- | ---: | --- |
| harmless | 0 | none |
| expected_generated_state | 5 | generated reports can carry source commit/provenance drift; stale managed-section validation wording was refreshed and rerun validation passed |
| expected_review_gate | 1 | AIDE-APPLY-01 and this checkpoint remain review-gated as designed |
| expected_dirty_pack_provenance | 1 | pack-status may record dirty source before checkpoint commit |
| fixture_only_patch | 1 | fixture patch behavior is intentional and does not authorize active repo apply |
| managed_section_note | 1 | accepted-with-notes because AIDE-APPLY-01 is a primitive, not full scoped apply readiness |
| assigned_next | 1 | latest task packet advances to AIDE-APPLY-02 |
| blocking | 0 | none |
| unknown_needs_review | 0 | none |

No target repo, branch/worktree, release publication, GitHub API, provider/model, network, Gateway, install apply, repair apply, upgrade apply, rollback/uninstall apply, active-repo managed-section apply, or active-repo transaction apply warning was observed.
