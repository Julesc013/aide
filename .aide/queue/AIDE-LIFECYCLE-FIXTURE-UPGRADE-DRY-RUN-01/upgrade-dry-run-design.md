# Upgrade Dry-Run Design

This WorkUnit is a static report-only upgrade dry-run check. It parses generated fixture plans and report examples, compares plan intent with scenario metadata, computes SHA-256 hashes for referenced checked-in files, and verifies no-mutation fields.

The check does not execute upgrade apply, lifecycle apply, scoped transaction apply against fixture targets, or any active repo apply. The generated upgrade reports under `.aide/reports/lifecycle-fixture-upgrade-dry-run/` are dry-run evidence, not apply evidence.

Allowed paths are limited to this task directory, `.aide/reports/lifecycle-fixture-upgrade-dry-run/**`, queue index, latest task packet, and deterministic status report refreshes. Protected paths include `.git/**`, `.github/**`, `.aide.local/**`, secret or credential files, target repositories, release roots, provider/model/Gateway surfaces, branch/worktree automation files, active lifecycle apply implementation files, scoped transaction executor implementation files, managed-section implementation files, and `core/**`.

Capability labels are limited to `upgrade-dry-run-checked`, `upgrade-report-checked`, `fixture-upgrade-planned`, `dry-run-planned`, `report-backed`, `schema-validated`, `locally-validated`, and `review-gated`. Upgrade apply and lifecycle apply remain planned-only.
