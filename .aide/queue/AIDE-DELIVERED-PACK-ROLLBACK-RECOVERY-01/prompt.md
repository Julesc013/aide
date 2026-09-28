# Owner-requested lifecycle recovery slice

The campaign requires actual supported rollback and recovery after
interruption. The current `rollback-pack` reports `RECOVERY_REQUIRED` for a
partial rollback intent but exposes no rollback-specific continuation.
Add an exact, explicit continuation through the existing guarded importer
recovery machinery; retain all source, artifact and effect gates.
