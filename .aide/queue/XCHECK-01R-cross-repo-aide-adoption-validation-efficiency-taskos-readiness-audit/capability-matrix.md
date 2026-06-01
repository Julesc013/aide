# Capability Matrix

| Capability | AIDE Source | Dominium Target | Eureka Target | Classification |
|---|---|---|---|---|
| Core AIDE doctor/validate/test/selftest | present and passing | present by reports | present by reports | available |
| Export/release bundle validation | present and passing | adopted from local bundle | adopted from local bundle | available with drift |
| Install/repair/upgrade/rollback/uninstall planning | present, no-apply | present by reports | present by reports | report-only available |
| Git/changelog/GitHub advisory | present, no-publish/no-mutation | target-local evidence exists | target-local evidence exists | report-only available |
| Existing-tool absorption | present, no-execution planning | XStack/AuditX/RepoX/TestX-like systems preserved/wrapped as candidates | tool capability map present | partial target-specific |
| Validation tiers | missing canonical AIDE policy | target-local tier model exists | full-suite/impacted status not canonicalized for AIDE | missing in AIDE |
| Async test telemetry | missing canonical AIDE executor/reducer/schema | partial timing/sharding evidence | not canonical as AIDE telemetry | missing |
| Task OS lifecycle schemas | missing canonical AIDE policies | target-local WorkUnit/dev-main/checkpoint/capability work exists | product WorkUnit runtime exists | not canonical in AIDE |
| Capability reality ledger | missing canonical AIDE policy | target-local capability reality ledger exists | fixture/live boundaries are explicit in product reports | partial outside AIDE |
| Apply automation | forbidden/deferred | not audited for sync | not audited for sync | not ready |

Source AIDE should build validation tiering first, then report-only Task OS
schemas and commands. Target-local Task OS-like work is evidence, not source
truth for AIDE.
