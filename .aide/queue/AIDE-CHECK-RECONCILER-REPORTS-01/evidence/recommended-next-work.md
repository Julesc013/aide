# Recommended Next Work

Recommended next task: `AIDE-ACCEPT-RECONCILER-REPORTS-01`

Reason:

- The build task exists, is indexed, and is stopped at `needs_review`.
- Reconciler reports and validation are present.
- CLI behavior is report-only and bounded.
- Focused tests and validation pass or pass with expected warnings.
- No blockers were found in this check.

Do not proceed directly to CapabilityManifest from this check. CapabilityManifest remains downstream only after a separate acceptance gate for Reconciler.
