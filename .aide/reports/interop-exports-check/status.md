# Interop Exports Check Status

Task: `AIDE-CHECK-INTEROP-EXPORTS-01`

Checked task: `AIDE-BUILD-INTEROP-EXPORTS-01`

Checked commit: `2a18e7c69966d06ffdd53e9fad357f61107cd37f`

Result: `PASS_WITH_WARNINGS`

Review gate: `needs_review`

The independent check verified that the static interop export previews exist,
their recorded SHA-256 hashes match the artifact bytes, JSON preview/report
artifacts parse, queue authority is preserved, and explicit non-capabilities are
retained.

No material findings were identified.

Recommended next task:

```text
AIDE-ACCEPT-INTEROP-EXPORTS-01
```
