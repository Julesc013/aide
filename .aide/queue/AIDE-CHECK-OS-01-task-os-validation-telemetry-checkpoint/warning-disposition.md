# Warning Disposition

## Result

All warnings are classified.

| Class | Count | Disposition |
| --- | ---: | --- |
| harmless | 2 | `test plan` exact form unsupported, and `test summary-validate` needs `--file`; supported equivalents passed. |
| expected_review_gate | 6 | AIDE-CONTINUE-00, X-TEST-00, X-OS-00, X-OS-01, X-OS-02, and AIDE-CHECK-OS-01 remain review-gated. |
| expected_generated_state | 2 | validation commands refreshed generated reports; changelog preview reports malformed historic commits for review. |
| expected_dirty_pack_provenance | 2 | pack-status and git plan record dirty source before the checkpoint commit. |
| deferred_target_work | 4 | X-TEST-01, X-TEST-03, target sync, and target pilots remain deferred. |
| capability_overclaim_warning | 1 | non-blocking capability wording review. |
| assigned_next | 1 | next task is assigned to focused Task OS report-consistency repair. |
| blocking | 1 | Task OS checkpoint/next-plan generated reports are stale relative to X-OS-02 truth. |
| unknown_needs_review | 0 | none. |

## Blocking Warning

The blocking warning is report-consistency only. It does not indicate apply behavior, target mutation, provider/model/network calls, or failed validation.
