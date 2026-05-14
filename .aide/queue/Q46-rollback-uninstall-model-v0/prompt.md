# Q46 Prompt Summary

Implement Rollback / Uninstall Model v0 in AIDE.

Q46 must observe current AIDE install state, inspect ownership and prior
install/upgrade/repair plans, classify AIDE-owned, target-owned, generated,
manual, local, and unknown files, then produce deterministic no-apply rollback
and uninstall plans, dry-run reports, policies, schemas, commands, tests,
golden tasks, docs, export-pack support, and evidence.

Q46 must not roll back files, uninstall files, remove managed sections, delete
`.aide`, overwrite target state, migrate files, move files, rewrite references,
mutate target repositories, mutate branches, publish releases, activate CI, or
call providers/models/network.
