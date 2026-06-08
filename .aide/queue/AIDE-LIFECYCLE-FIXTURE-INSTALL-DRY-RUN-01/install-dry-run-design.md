# Install Dry-Run Design

This WorkUnit uses static report-only checks. It parses generated install lifecycle fixture plans, fixture scenario metadata, generated plan reports, expected report examples where present, target baselines, expected states, and hash references.

It does not introduce a `lifecycle-install` command and does not alter `.aide/scripts/aide_lite.py`. Command support is deferred to a future WorkUnit if queue authority explicitly permits script and test paths.

The reports under `.aide/reports/lifecycle-fixture-install-dry-run/` are check evidence, not apply evidence. They state `report_only=true`, `dry_run=true`, `install_apply_executed=false`, `lifecycle_apply_executed=false`, `scoped_transaction_apply_executed=false`, `target_files_mutated=false`, and `review_gate=needs_review`.
