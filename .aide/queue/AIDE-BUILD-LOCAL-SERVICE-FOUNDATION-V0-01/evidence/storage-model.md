# Storage Model

SQLite tables:

- `migrations`
- `objects`
- `events`
- `artifact_metadata`
- `idempotency`
- `cursors`

Filesystem payloads:

- content-addressed payloads under `artifacts/sha256/<prefix>/<digest>`
- temporary payload writes under `temp/`

The fixture uses temporary directories by default. Operator-provided runtime
state belongs under ignored `.aide.local/service/**`.
