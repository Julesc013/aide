# OKF Integration Review

OKF integration is read-only.

The projection attaches OKF refs for existing capability knowledge pages and
does not refresh or rewrite `.aide/knowledge/okf/**`.

Known warnings remain:

- latest task packet is stale
- OKF source hashes can lag current queue/report state

These are classified as non-blocking Reconciler warnings and are not repaired by
CapabilityManifest.
