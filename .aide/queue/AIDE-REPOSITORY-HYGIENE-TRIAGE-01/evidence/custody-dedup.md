# Verified Loose Custody Suppression

## AIDE-FACMAN-USK-ZIP-INTEGRATION-01

- Loose files checked: 62.
- Loose hash mismatches: 0.
- Tracked archive entries checked: 131.
- Archive member mismatches: 0.
- Archive SHA-256 matched its tracked custody record.

## AIDE-FACMAN-USK-STREAMING-INTEGRATION-01

- Loose files checked: 40.
- Loose hash mismatches: 0.
- Tracked archive entries checked: 67.
- Archive member mismatches: 0.
- Archive SHA-256 matched its tracked custody record.

The loose files remain on disk and in the external recovery snapshot. Narrow
task-specific ignore rules remove them from ordinary Git status because their
exact bytes are already present in tracked custody archives. No deletion or
global evidence-ignore rule is authorized by this result.
