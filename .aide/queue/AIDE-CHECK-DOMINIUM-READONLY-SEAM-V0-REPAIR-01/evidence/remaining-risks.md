# Remaining Risks

The repair check result is `REQUEST_CHANGES`.

Remaining material gaps:

- Diagnostic projection disclosure is incomplete.
- Refusal projection disclosure is incomplete.
- Public schema does not constrain kind-specific `spec` fields.
- Public schema does not constrain status facts.
- One or more replayable negative fixtures failed independent replay.
- Conformance results lack required independent assertion fields.
- Demo operation ledger lacks `allowed_operation_count`.
- Demo operation ledger lacks instrumentation coverage.
- Demo operation ledger does not describe every required operation family.
- Cross-process determinism failed in the independent replay.

These gaps block seam acceptance and route to `AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.
