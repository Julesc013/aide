# Scenario Plan Review

| Scenario | Phase | Plan State | Expected Status | Expected Blocker | Mutation State | Interlock |
| --- | --- | --- | --- | --- | --- | --- |
| install-clean | install | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| install-existing-manual-preserved | install | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| install-managed-section | install | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| upgrade-v2 | upgrade | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| upgrade-manual-preserved | upgrade | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| drift-detected | upgrade | accepted_with_notes | BLOCKED | BLOCKED_DRIFT_DETECTED | blocked_no_mutation | apply_mode_authorized=false |
| repair-plan-missing-marker | repair | accepted_with_notes | BLOCKED | BLOCKED_MARKER_MISSING | blocked_no_mutation | apply_mode_authorized=false |
| repair-plan-malformed-marker | repair | accepted_with_notes | BLOCKED | BLOCKED_MARKER_MALFORMED | blocked_no_mutation | apply_mode_authorized=false |
| rollback-record-generated | rollback | accepted_with_notes | PASS_WITH_WARNINGS | none | static_record_only | apply_mode_authorized=false |
| uninstall-manual-preserved | uninstall | accepted_with_notes | PASS_WITH_WARNINGS | none | static_fixture_only | apply_mode_authorized=false |
| protected-path-blocked | install | accepted_with_notes | BLOCKED | BLOCKED_PROTECTED_PATH | blocked_no_mutation | apply_mode_authorized=false |
| traversal-blocked | install | accepted_with_notes | BLOCKED | BLOCKED_PATH_TRAVERSAL | blocked_no_mutation | apply_mode_authorized=false |
| broad-delete-blocked | uninstall | accepted_with_notes | BLOCKED | BLOCKED_BROAD_DELETE | blocked_no_mutation | apply_mode_authorized=false |

Residual risk is the same for all scenarios: these plans are static planning artifacts and have not been executed by a lifecycle dry-run harness or fixture apply executor.
