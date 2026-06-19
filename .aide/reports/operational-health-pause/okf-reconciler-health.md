# OKF And Reconciler Health

## OKF

- `okf validate`: `PASS_WITH_WARNINGS`
- `okf lint`: `PASS_WITH_WARNINGS`
- broken_links_count: 0
- orphan_pages_count: 0
- missing_source_refs_count: 0
- missing_evidence_refs_count: 0
- stale_context_findings_count: 1
- projection_only: true

## Reconciler

- `reconciler status`: `PASS_WITH_WARNINGS`
- `reconciler validate`: `PASS_WITH_WARNINGS`
- findings_count: 4
- report_only: true
- detects_drift: true
- repair_implemented: false
- mutation_performed: false

## Disposition

OKF and Reconciler are usable as predecessor context for PatchTransaction. They
do not provide repair authority, source-truth mutation, profile activation,
admission, trust, or runtime orchestration.
