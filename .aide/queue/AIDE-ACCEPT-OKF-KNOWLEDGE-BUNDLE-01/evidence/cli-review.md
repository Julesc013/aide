# CLI Review

Result: `ACCEPTED_WITH_WARNINGS`.

Accepted CLI surface:

- `okf status`
- `okf project --source current-repo`
- `okf validate`
- `okf lint`

The CLI remains a thin deterministic projection/report/validation surface.

Focused tests reject runtime or network-shaped OKF subcommands such as `serve`, `crawl`, `enrich`, `llm-update`, `search-index`, `vector-index`, `visualize`, and `sync-remote`.

No live service, crawler, provider/model call, network enrichment, graph runtime, search/vector index, remote sync, branch/worktree automation, target mutation, release action, or GitHub mutation is accepted.
