# Atomicity Model

- object update plus event append is performed in one SQLite transaction
- injected failure between object write and event append rolls back the object
- artifact payload bytes are written and verified before metadata is recorded
- payload persistence uses a temporary file and atomic replace

This is local atomicity only, not distributed transaction semantics.
