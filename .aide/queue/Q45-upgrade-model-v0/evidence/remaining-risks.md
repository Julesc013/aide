# Remaining Risks

- Q45 has no apply mode; it cannot upgrade a real target repo yet.
- No Eureka, Dominium, or other target repo upgrade was performed.
- No rollback/uninstall model exists yet; Q46 is required before upgrade plans have a paired rollback/uninstall contract.
- No release bundle was published.
- Upgrade planning is deterministic and local, but still heuristic where ownership, generated state, and compatibility are ambiguous.
- Source-pack comparison currently records eight source-state leak blockers that require future review before any apply-capable phase.
- Optional migrations are advisory only and intentionally deferred.
- Target repositories must generate their own upgrade observations, comparisons, plans, dry-runs, and evidence.
- `core/gateway/tests` did not complete within the 120 second validation timeout and remains a recorded validation gap.
