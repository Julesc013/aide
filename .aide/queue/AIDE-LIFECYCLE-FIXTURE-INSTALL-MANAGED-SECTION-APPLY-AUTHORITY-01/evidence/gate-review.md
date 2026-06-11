# Gate Review

The apply gate selected:

- scenario: `install-managed-section`
- operation: `update_managed_section`
- target path: `manual/with-managed-section.md`
- future task: `AIDE-LIFECYCLE-FIXTURE-INSTALL-MANAGED-SECTION-APPLY-01`

It also explicitly set `apply_authorized_by_this_gate: false`, so a separate authority task was required before mutation.

This authority task supplies that separate decision.
