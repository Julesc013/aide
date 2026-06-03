# Managed Section Review

- result: ACCEPTED_WITH_NOTES
- reviewed_task: AIDE-APPLY-01-managed-section-patcher
- status_reviewed: needs_review

## Findings

- Marker policy requires explicit `AIDE-GENERATED` begin/end markers and blocks ambiguous marker state.
- Ownership policy treats generated content inside valid markers as AIDE-owned and manual content outside markers as user-owned.
- Schemas and examples exist for managed-section operations, patch reports, conflicts, and fixture reports.
- `core/apply/managed_sections.py` implements parsing, patch planning, in-memory patch application, manual-content preservation checks, fixture-safe path handling, and fixture-only file patching.
- The implementation does not expose active repository apply, target mutation, branch/worktree mutation, GitHub mutation, provider/model/network calls, Gateway forwarding, or install/repair/upgrade/rollback/uninstall apply behavior.

## Notes

- Acceptance is not production apply readiness. AIDE-APPLY-02 must add explicit transaction executor gates before any real repo mutation is allowed.
- Existing fixture patch behavior is intentionally limited to test/fixture roots.
