# Q18 Cache Key Report

## Latest Artifacts

- JSON: `.aide/cache/latest-cache-keys.json`
- Markdown: `.aide/cache/latest-cache-keys.md`

## Surfaces Keyed

- latest task packet
- latest context packet
- latest review packet
- latest verification report
- latest route decision
- latest golden tasks report
- token savings summary

## Current Metadata Summary

- key count: 7
- contents inline: false
- raw prompt storage: false
- raw response storage: false
- local state ignored: true
- tracked local-state paths: 0
- git commit in latest report: current committed Q18 docs/cache state when `cache report` was run
- dirty state in latest report: true, expected because Q18 evidence/generated artifacts were still being refreshed

## Determinism Notes

- File content hashes use SHA-256.
- Cache key IDs include the surface, content hash, and deterministic dependency metadata.
- Stable serialization is used for key seed material.
- Re-running `cache key --file .aide/context/latest-task-packet.md` and `cache key --task-packet .aide/context/latest-task-packet.md` produced the same key for the same file state.
- Unit tests cover key stability and key changes when content changes.

## Refusal Behavior

The cache-key helper refuses:

- `.env`
- `.aide.local/**`
- `secrets/**`
- ignored paths such as `node_modules/**`
- missing paths
- directories
- binary-like files

## Budget Notes

The compacted cache-key JSON report is near the evidence budget but no longer over budget. The token ledger currently reports:

- near budget: cache report `.aide/cache/latest-cache-keys.json`
- near budget: existing Q17 validation evidence

## Limitations

- Dependency hashes are conservative metadata, not a complete semantic invalidation system.
- Policy-version metadata is compacted in the committed report to avoid turning cache keys into an oversized artifact.
- Cache metadata does not prove safe reuse by itself.
