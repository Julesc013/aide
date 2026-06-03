# Remaining Risks

- AIDE-APPLY-01 is accepted with notes only; it does not prove broad active-repo apply readiness.
- Generated reports can carry source-commit/provenance drift until refreshed by deterministic commands and committed.
- Export-pack content is source-side portable support and evidence, not target repository truth.
- Rollback records are evidence-only; rollback/uninstall apply remains forbidden.
- AIDE-APPLY-02 must add explicit executor gates before any real repository mutation can be considered safe.
