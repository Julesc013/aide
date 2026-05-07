# Export / Import State

## Pack Inventory

Path: `.aide/export/aide-lite-pack-v0/`

| Artifact | State |
| --- | --- |
| `manifest.yaml` | present |
| `checksums.json` | present |
| `install.md` | present |
| `import-policy.yaml` | present |
| `README.md` | present |
| `export-report.md` | present |
| `files/` payload | present |

Latest export report records:

- included files: 122
- checksums: 126
- boundary result: PASS
- provider/model calls: none
- network calls: none
- raw prompt storage: false
- raw response storage: false

## Portable Includes

- AIDE Lite script and portable tests.
- token, context, verifier, evidence, ledger, eval, controller, routing, cache,
  local-state, Gateway, provider, export/import, and adapter policies.
- prompts and review templates.
- starter golden tasks.
- target-neutral profile and memory templates.
- adapter templates and target definitions.
- install/import docs.

## Portable Excludes

The pack excludes source-specific state:

- `.aide/profile.yaml` from AIDE source
- `.aide/queue/**`
- `.aide/memory/project-state.md`
- generated context and latest packets
- reports and token ledgers
- controller/outcome ledgers
- route decisions
- cache-key reports
- gateway/provider status reports
- eval runs
- local state and `.aide.local/`
- `.env`
- raw prompts and raw responses
- secrets and provider keys

## Fixture Import Evidence

Q21 evidence records a successful temporary fixture import:

- dry-run: PASS
- import: PASS
- existing AGENTS manual content preserved
- target-specific memory templates created
- `.aide.local/` ignored and not created
- target doctor/snapshot/index/pack/estimate ran
- fixture task packet: 3,789 chars / 948 approximate tokens

## Current Pack Warnings

- `manifest.yaml` records `source_dirty_state: true` because the audit command
  sweep refreshed generated/report artifacts before `export-pack` was run.
- Fixture import is not target repo proof. Eureka and Dominium still require
  real import pilots.
