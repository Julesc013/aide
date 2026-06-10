# Remaining Risks

- Six static expected-report refs are absent and should be repaired before fixture apply gate planning.
- The global `task next-plan` selector may still point at `AIDE-APPLY-LIFECYCLE-PLAN-01`; task-local closure authority selects `AIDE-LIFECYCLE-EXPECTED-REPORT-GAP-REPAIR-01`.
- Lifecycle apply, fixture apply, active repo apply, and target repo apply remain unimplemented or unauthorized.
- Any future fixture apply gate still needs a separate reviewed WorkUnit after expected-report gap repair.
