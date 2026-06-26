# Fixture Coverage Review

The source fixture corpus covers compact valid ledgers, extension round-trip,
duplicate record ids, unknown classes, vendor digest requirements, managed
section identity, unknown/never-touch apply flags, unsafe paths, source latest
contamination, unknown required features, and required extension rejection.

Required check-oracle fixtures are missing for:

- vendor-managed file matching digest and drift.
- managed-section missing markers, duplicate markers, overlapping sections, and
  identity mismatch.
- manual text outside managed section preservation.
- project overlay, generated output, runtime generated, local only,
  evidence-only, preserved legacy, never touch as direct fixture cases.
- case-fold collision, path collision, symlink path, reparse path, and nested
  ownership conflict.
- Q43 migration complete, manual-review, unknown, and unmapped cases.

Disposition: material finding `ownership.fixture_coverage_incomplete`.
