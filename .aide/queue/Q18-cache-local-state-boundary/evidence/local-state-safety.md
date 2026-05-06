# Q18 Local-State Safety

## Boundary

- Committed contract and reviewable metadata root: `.aide/`
- Gitignored local runtime state root: `.aide.local/`
- Safe example layout root: `.aide.local.example/`

## Ignore Status

- `.gitignore` exists.
- `.gitignore` includes `.aide.local/` and `.aide.local/**`.
- `git check-ignore .aide.local/` reports `.aide.local/`.
- AIDE Lite `cache status` reports `tracked_local_state_paths: 0`.

## Example Layout

- `.aide.local.example/README.md`
- `.aide.local.example/config.example.yaml`
- `.aide.local.example/cache/README.md`
- `.aide.local.example/traces/README.md`
- `.aide.local.example/secrets/README.md`
- `.aide.local.example/ledgers/README.md`

The example layout contains no provider keys, secrets, raw prompts, raw responses, traces, or cache blobs.

## Safety Rules

- Future provider keys must remain local only.
- Raw prompt and raw response storage is disabled by default.
- Actual `.aide.local/` contents must never be committed.
- Cache reports under `.aide/cache/**` are metadata only.
- Cache hits must not bypass verifier, golden tasks, route hard floors, or review gates.

## Tracked-Local-State Check

Current AIDE Lite status reports no tracked or staged `.aide.local/` paths. If future work accidentally stages `.aide.local/**`, `cache status`, `validate`, and `verify` are expected to flag it.

## Future Gateway/Service Implication

Future Gateway or Runtime work must respect this boundary. It may reference `.aide.local/` as local state, but Q18 does not authorize creating committed runtime cache content, provider credentials, raw prompt logs, or response logs.
