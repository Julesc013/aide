# Baseline

- AIDE local source: 7d8bf19d878fd9ad29859a6cba4b7de64ad80ecc, initially clean.
- Windows inspection identity: BLACKGLASS-WIN1\\CodexSandboxOffline. No user-context GitHub authentication claim made.
- Installed primary Codex CLI: 0.145.0; exec JSON, output-schema and explicit resume IDs confirmed with local help and official noninteractive documentation.
- inspect/noop/recover: task missing before admission, as expected for a new work item.
- Dedicated state schema is required: accepted SQLiteStore uses fixture timestamps and its optimistic SELECT/update pair does not provide the coordinator's atomic claim semantics.
- FacMan protected_dev_merge_active and delegated_dev_merge are false. This implementation cannot legitimately treat integration as enabled.
