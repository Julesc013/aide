# Remaining Risks

## Implementation Risks

- AIDE-APPLY-02 is authorized for implementation but not implemented by this task.
- AIDE-APPLY-01 and AIDE-CHECK-APPLY-01 remain `needs_review`; their evidence records `ACCEPTED_WITH_NOTES` and `READY_FOR_AIDE_APPLY_02_WITH_WARNINGS`, but broader acceptance still requires review discipline.
- Existing transaction schemas are deliberately not in the AIDE-APPLY-02 allowlist. If implementation needs to change them, it must stop for permission widening.
- Existing managed-section implementation `core/apply/managed_sections.py` is deliberately not in the allowlist. If integration requires modifying it, implementation must stop for permission widening.
- Dry-run/report behavior must be kept distinct from apply evidence so report-only outputs are not misread as mutation capability.
- Generated report churn from AIDE Lite status commands must be restored unless generated reports are intentionally changed inside an authorized implementation path.

## Deferred Surfaces

- install apply;
- upgrade apply;
- repair apply;
- rollback/uninstall apply;
- target repo mutation;
- branch/worktree mutation;
- merge;
- push;
- promotion;
- release publication;
- GitHub mutation;
- provider/model calls;
- Gateway calls;
- network calls;
- broad active-repo apply.
