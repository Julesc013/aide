# CLI Review

Added thin AIDE Lite dispatch:

- `reconciler status`
- `reconciler report`
- `reconciler validate`

The CLI prints report-only boundary lines and delegates behavior to `core/reconciler/reconciler_reports.py`.

Rejected by parser tests:

- `reconciler repair`
- `reconciler apply`
- `reconciler fix`
- `reconciler mutate`
- `reconciler serve`
- `reconciler schedule`
- `reconciler run`
- `reconciler sync`
