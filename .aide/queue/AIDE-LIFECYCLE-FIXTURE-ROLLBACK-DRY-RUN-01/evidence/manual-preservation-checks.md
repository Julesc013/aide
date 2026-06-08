# Manual Preservation Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/manual-preservation-checks.json`

Result: `PASS`

Managed section preservation:

- The generic example and install rollback record state that outside-marker content is not owned by AIDE.

Generated-file preservation:

- The upgrade rollback record states that the fixture generated file is AIDE-owned and manual files remain out of scope.

Unknown file/delete behavior:

- Unknown ownership remains a stop condition.
- Broad delete remains unsupported and blocked.

No manual content mutation was performed.
