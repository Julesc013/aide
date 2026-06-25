# Persistence

The fixture writes local Service state to a temporary SQLite database, closes
the store, reopens it, and verifies:

- persisted AuthorizationEvaluation
- persisted CapabilityGrant status and remaining uses
- monotonic event sequences
- no committed `.aide.local` runtime state

The committed reports contain normalized data and relative evidence paths only.
