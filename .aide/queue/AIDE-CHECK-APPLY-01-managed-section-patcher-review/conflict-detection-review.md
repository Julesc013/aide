# Conflict Detection Review

- result: PASS_WITH_WARNINGS
- ambiguous_marker_patch_blocked: true
- unsupported_file_patch_blocked: true

## Reviewed Conflict Classes

- missing start marker: blocked
- missing end marker: blocked
- duplicate marker: blocked
- nested marker: blocked
- malformed marker: blocked
- unsupported/binary file: blocked or unsupported
- existing hash mismatch: blocked

## Evidence

- Managed-section policies list marker and ownership conflict classes.
- Core tests cover missing, duplicate, nested, malformed, binary, and existing-hash mismatch behavior.
- Conflict reports record blocked fixture cases and do not patch active repository files.

## Note

AIDE-APPLY-02 should not broaden conflict recovery. Unknown or ambiguous marker state should continue to block mutation.
