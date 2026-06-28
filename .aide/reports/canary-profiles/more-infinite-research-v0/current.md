# More Infinite Research Canary Profile v0

## Result

- result: `PARTIAL`
- material_finding_count: `0`
- missing_evidence: `0`
- recommended_next_task: `AIDE-BUILD-CANARY-PROFILE-MORE-INFINITE-RESEARCH-INPUTS-01`

## Target Identity

- repository: `Julesc013/more-infinite-research`
- URL: `https://github.com/Julesc013/more-infinite-research`
- type: `factorio_mod`
- language: `Lua`
- target source type: `public_metadata`
- local target availability: `unavailable`

No local checkout was found under `C:/Projects`, so this profile is public-metadata-only and does not claim local canary readiness.

## Operator Priority

The operator prioritized More Infinite Research before ScreenSave for immediate practical downstream canary work. This task records that priority without rewriting the accepted distribution product-status projection history.

## Factorio Mod Metadata

- `name`: `more-infinite-research`
- `version`: `1.2.10`
- `factorio_version`: `2.1`
- dependencies: `base >= 2.0`, optional `space-age`, optional `Better_Robots_Extended`
- latest GitHub release observed: `1.2.9`

Source `info.json` is ahead of the latest GitHub release observed from public metadata. This is useful canary evidence and requires operator review before any future release planning.

## File Inventory

- entry points: `data.lua`, `data-updates.lua`, `settings.lua`
- configuration: `defaults.lua`
- metadata: `info.json`, `README.md`, `LICENSE`, `TODO.txt`, `thumbnail.png`
- locale: `locale/**`
- prototypes: `prototypes/**`

## Ownership Classification

- project_owned: `README.md`, `LICENSE`, `TODO.txt`, `info.json`, `thumbnail.png`, Lua entry points, `defaults.lua`, `locale/**`, `prototypes/**`
- generated_or_regenerable: none identified from public metadata
- vendor_managed_candidate: none identified from public metadata
- local_only: unknown without local checkout
- evidence_only: AIDE canary profile reports and task evidence
- protected: `info.json`, `LICENSE`, `README.md`, `thumbnail.png`, release tags, published release assets
- unknown: local untracked files, ignored files, generated release artifacts, Factorio runtime output
- never_touch: `.git/**`, `.aide.local/**`, credentials, Factorio user data, published release assets

## Validation Candidates

- parse `info.json` as JSON
- validate Factorio mod name/version/factorio_version fields
- check Lua syntax when a Lua interpreter is configured
- check locale key coverage
- check `defaults.lua` and `settings.lua` consistency
- check release/source version drift
- dry-run package zip naming only after explicit archive task authorization

Missing dependencies: local MIR checkout path, Lua executable configuration, Factorio executable/headless validation configuration.

## Blockers

- local target checkout path is not configured
- local clean/dirty state cannot be verified
- shadow apply is not accepted
- MIR UpdatePlan and RollbackBundle are not built
- real target apply and branch/worktree automation remain non-capabilities
- release generation and publication are not authorized

## Explicit Non-Capabilities

- no MIR mutation
- no real target apply
- no shadow apply
- no release generation
- no release publication
- no mod portal upload
- no GitHub Release publication
- no branch/worktree automation
- no provider/model calls
- no package-source fetching
- no automatic version bump
- no automatic zip publish

## Source Refs

- `https://api.github.com/repos/Julesc013/more-infinite-research`
- `https://raw.githubusercontent.com/Julesc013/more-infinite-research/main/info.json`
- `https://api.github.com/repos/Julesc013/more-infinite-research/releases/latest`
- `https://api.github.com/repos/Julesc013/more-infinite-research/git/trees/main?recursive=1`
- `https://lua-api.factorio.com/latest/auxiliary/mod-structure.html`
