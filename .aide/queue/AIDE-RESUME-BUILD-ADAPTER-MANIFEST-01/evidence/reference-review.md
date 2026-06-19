# Reference Review

Adapter identity uses `aide://adapter/minimal-local-disposable-worker-declaration-01`.

The manifest record uses `aide://artifact/...` as artifact identity and
references capability, conformance-result, and evidence refs as prerequisites
only. Wrong-kind refs fail closed in focused tests. Presence of a
ConformanceResult ref does not set `trusted: true`.
