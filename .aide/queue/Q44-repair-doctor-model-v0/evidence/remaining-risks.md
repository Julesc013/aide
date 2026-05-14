# Remaining Risks

- Q44 is no-apply only. It cannot repair a broken target install by itself.
- No real Eureka, Dominium, or external target repair was performed.
- No install, upgrade, rollback, or uninstall apply behavior exists yet.
- No release bundle is published by Q44.
- Repair classes and detection are deterministic heuristics; target repos must generate and review their own repair observations.
- Missing/stale portable file findings are candidate future repair operations, not approval to restore or overwrite files.
- Pack provenance remains `DIRTY_SOURCE_RECORDED` until Q44 is committed and the pack is regenerated in a clean source state by a future phase or operator action.
- Q45 Upgrade Model v0 is needed next so stale or older AIDE installs can be upgraded by plan, not by ad hoc repair or overwrite.
