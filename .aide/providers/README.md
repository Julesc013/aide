# AIDE Provider Adapter Metadata

Q20 defines provider adapter contracts and provider-family metadata only. This
directory is a committed repo contract for offline validation; it is not a
credential store, provider configuration directory, live model registry, or
Gateway proxy configuration.

## Files

- `provider-catalog.yaml`: provider-family metadata, not live accounts.
- `capability-matrix.yaml`: conservative capability dimensions and statuses.
- `adapter-contract.yaml`: expected adapter metadata shape for future phases.
- `status.yaml`: Q20 no-call provider-adapter state.
- `latest-provider-status.json`: generated compact provider metadata report.
- `latest-provider-status.md`: generated compact human-readable provider report.

## Boundaries

- Live provider calls are disabled in Q20.
- Model calls and provider probes are disabled in Q20.
- Provider credentials must never be committed.
- Future credential references belong under gitignored `.aide.local/`.
- Gateway forwarding remains deferred to a future reviewed queue phase.
