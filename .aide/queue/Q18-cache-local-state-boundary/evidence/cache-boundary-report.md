# Q18 Cache Boundary Report

## Summary

Q18 defines a deterministic cache boundary without implementing a live cache. The committed repo now has cache/local-state policy, a safe example local-state layout, cache-key metadata reports, and AIDE Lite cache commands.

## Policy Files

- `.aide/policies/cache.yaml`
- `.aide/policies/local-state.yaml`
- `.aide/cache/key-policy.yaml`

## Cache Classes

The Q18 cache policy names these classes:

- context packet
- task packet
- review packet
- verification report
- route decision
- tool result
- provider response
- semantic answer
- local KV metadata

Only deterministic metadata reports are committed. Provider response and semantic answer caches are disabled by default.

## Key Inputs

Cache-key metadata may include:

- git commit when available
- dirty-state flag
- content SHA-256
- dependency hashes
- task/context/review/verification/route artifact hashes
- policy-version hashes
- command argument hash in future work
- provider/model identifiers only if a future reviewed phase enables them

Current key format:

```text
aide-cache-v0:<surface>:<short_sha256>
```

## Invalidation Rules

- File hash changes invalidate related packet keys.
- Policy changes invalidate route/cache keys.
- Context compiler changes invalidate context keys.
- Verifier changes invalidate verification keys.
- Dirty git state marks key metadata dirty.
- Stale or unknown cache metadata must not be trusted.

## Commands Added

- `cache init`
- `cache status`
- `cache key --file PATH`
- `cache key --task-packet PATH`
- `cache report`

All commands are standard-library only and make no provider, model, network, Gateway, or Runtime calls.

## Generated Reports

- `.aide/cache/latest-cache-keys.json`
- `.aide/cache/latest-cache-keys.md`

The JSON report is compact metadata. The Markdown report is the human-readable summary. Neither stores raw prompt or response content.

## Deferred Cache Behavior

- No live provider response cache.
- No semantic cache for code edits.
- No embeddings/vector index.
- No local model KV cache.
- No Gateway/runtime cache service.
- No exact-token cache or billing ledger.

## Limitations

Cache keys are useful for detecting identity and dependency changes, but they are not permission to reuse content. Verifier, review gates, golden tasks, and route hard floors still apply.
