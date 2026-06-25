# Service Boundary

Implemented:

- local SQLite object/event/idempotency/cursor store
- local artifact metadata table
- local filesystem content-addressed artifact store
- fixture-only AIDE Lite commands
- generated reports under `.aide/reports/local-service-foundation-v0/`

Not implemented:

- network API
- HTTP server
- socket listener
- scheduler
- worker execution
- capability execution
- trust enforcement
- MCP runtime
- Workbench runtime
- distributed locking
- provider/model calls
- preview/apply/rollback
- repository mutation
