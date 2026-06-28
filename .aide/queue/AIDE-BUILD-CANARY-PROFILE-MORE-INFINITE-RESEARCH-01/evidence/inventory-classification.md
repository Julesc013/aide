# Inventory Classification

Public file tree included:

- entry points: `data.lua`, `data-updates.lua`, `settings.lua`
- configuration: `defaults.lua`
- metadata: `info.json`, `README.md`, `LICENSE`, `TODO.txt`, `thumbnail.png`
- locale files under `locale/**`
- prototype files under `prototypes/**`

Ownership classification:

- project_owned: source Lua files, locale files, metadata, README, LICENSE, thumbnail
- generated_or_regenerable: none identified from public metadata
- vendor_managed_candidate: none identified from public metadata
- local_only: unknown without local checkout
- evidence_only: AIDE reports and task evidence
- protected: `info.json`, `LICENSE`, `README.md`, `thumbnail.png`, release tags, published release assets
- unknown: local untracked files, ignored files, generated release artifacts, Factorio runtime output
- never_touch: `.git/**`, `.aide.local/**`, credentials, Factorio user data, published release assets
