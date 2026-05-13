# Export Pack Readiness

## Current Pack

- Path: `.aide/export/aide-lite-pack-v0`.
- Manifest: `.aide/export/aide-lite-pack-v0/manifest.yaml`.
- Checksums: `.aide/export/aide-lite-pack-v0/checksums.json`.
- Pack-status: PASS.
- Checksum problems: 0.
- Boundary violations: 0.
- Provenance result: `DIRTY_SOURCE_RECORDED`.
- Included files after export: 206.
- Checksum count after export: 209.
- Source commit recorded after export:
  `6246811cf02ece09bd25b53ce0625919db658f51`.

## Included Governance Classes

- Commit message policy.
- Commit hook template.
- Commit template.
- Changelog policy, config, templates, and command support.
- Task resumption policy.
- WorkUnit policy.
- Recovery policy.
- Git workflow policy.
- Branch roles policy.
- Promotion rules policy.
- Sync policy.
- Prune policy.
- Git helper policy and helper docs.
- Project workflow profiles.
- Portable golden tasks.
- Portable reference docs.
- AIDE Lite command implementation.

## Excluded Source-State Classes

- AIDE source queue history.
- AIDE source memory.
- Generated context/review packets.
- Generated source Git workflow detection and helper plans as target truth.
- Generated changelog preview outputs as target truth.
- `.aide.local/**`.
- Secrets, provider keys, raw prompt logs, raw response logs.

## Installability Verdict

The pack is valid and safe for controlled dry-run/targeted import. It is not
yet an automatic stable installer because the install/upgrade/rollback control
plane is missing.

## Required Before "Ultimate Stable Install"

- Install preflight schema.
- Ownership ledger.
- Conflict report schema.
- Apply plan schema.
- Verification report schema.
- Repair plan.
- Upgrade plan.
- Rollback plan.
- Uninstall plan.
- Release bundle/draft manifest.
