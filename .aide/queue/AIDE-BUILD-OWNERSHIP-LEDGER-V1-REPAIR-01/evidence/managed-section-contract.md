# Managed Section Contract

Managed-section records now include containing file, section identity, marker
format, start/end marker digests, section content digest, surrounding-content
preservation policy, preimage requirements, and update constraints.

Validation refuses missing section identity, mismatch between section identity
and managed-section identity, duplicate markers, overlapping sections, nested
sections without explicit precedence, unsafe containing-file paths, and
file-section ownership conflicts.

Report matrix:

```text
.aide/reports/ownership-ledger-v1-repair-01/managed-section-contract-matrix.json
```
