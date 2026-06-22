# Baseline

- Branch: `main`.
- Starting worktree after Phase A commit: clean, `main...origin/main [ahead 1]`.
- Phase A commit: `05cb2b82980d1dbb9fb18524f0ba191a460b7962`.
- Phase A task inspection: `missing_evidence: 0`, `status: needs_review`.
- Repair 04 check commit: `0dd7eabc10508fe4a15965495314a15eeb02e495`.
- Repair 04 check result: `REQUEST_CHANGES`, `material_finding_count: 4`.
- Repair 04 check blockers:
  - `schema.open_object_surfaces_bounded`
  - `extension.authority_names_semantically_refused`
  - `conformance.guard_evidence_exercised`
  - `operation.guard_report_not_static`
- Downstream task directories were absent before Phase B:
  - `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-05`
  - `AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`
  - `AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01`
- Dominium checkout was clean: `main...origin/main [behind 24]`.

The check is bounded to the four Repair 05 source findings, critical regression
sampling, production immutability, evidence truthfulness, and next-task routing.
