# Interop Exports Check Report

`AIDE-CHECK-INTEROP-EXPORTS-01` independently checked the static preview exports
created by `AIDE-BUILD-INTEROP-EXPORTS-01`.

Findings:

- Build task exists and is complete at `needs_review`.
- Build result is `PASS_WITH_WARNINGS`.
- Build task evidence reports `missing_evidence: 0`.
- Six static preview artifacts exist under `.aide/interop/exports/`.
- All six artifact hashes match `.aide/interop/exports/manifest.json`.
- Preview JSON and report JSON parse.
- Manifest and reports agree on artifact count, artifact paths, and hashes.
- Preview artifacts preserve queue authority and non-capability boundaries.
- Build artifacts were not modified by this check.

No material findings were found.

Result: `PASS_WITH_WARNINGS`.

Recommended next task: `AIDE-ACCEPT-INTEROP-EXPORTS-01`.
