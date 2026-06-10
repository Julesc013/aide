# Remaining Risks

- `uninstall-manual-preserved` lacks a static expected report ref.
- Uninstall execution is not implemented or executed.
- Broad-delete evidence is blocked metadata only.
- Scoped executor v0 does not provide uninstall/delete execution.
- Global `task next-plan` still selects `AIDE-APPLY-LIFECYCLE-PLAN-01`.

These risks do not block this dry-run WorkUnit, but the expected-report gap should be classified during proof closure.
