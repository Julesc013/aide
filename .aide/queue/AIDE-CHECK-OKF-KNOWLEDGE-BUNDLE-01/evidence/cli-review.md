# CLI Review

Result: `PASS_WITH_WARNINGS`.

The AIDE Lite CLI registers a narrow `okf` command group with:

- `okf status`
- `okf project --source current-repo`
- `okf validate`
- `okf lint`

Focused tests cover status, projection, validation, lint, JSON report parsing, and rejection of runtime or network-shaped subcommands such as `serve`, `crawl`, `enrich`, `llm-update`, `search-index`, `vector-index`, `visualize`, and `sync-remote`.

The CLI surface is report/projection-only. It does not add runtime knowledge serving, web crawling, model/provider calls, remote sync, branch mutation, target mutation, or GitHub mutation.
