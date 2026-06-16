# Reference Map Review

Result: PASS_WITH_WARNINGS.

Reviewed report:

- `.aide/reports/reference-id/reference-map.json`

Findings:

- `kind`: `ReferenceIDMap`
- Projected reference count: 25
- Grammar: `aide://<kind>/<id>`
- Recommended next task in build report: `AIDE-CHECK-REFERENCE-ID-SCHEME-01`
- All required locators exist.
- All required locators include SHA-256 metadata.
- All projected records report `status.valid: true`.
- File paths remain locators and are not used as identity.
- Optional future placeholders exist for `aide://event/future-event-placeholder` and `aide://patch-transaction/future-patch-transaction-placeholder` without claiming those object protocols exist.

Warnings:

- Reference map records future ref kinds syntactically but intentionally does not implement their protocols.
