# Q45 Prompt Summary

Implement Upgrade Model v0 in AIDE.

Q45 must observe the current installed AIDE state, observe the current source
export pack, compare installed state to source pack state, classify
compatibility and migration needs, preserve target-specific state, and produce
deterministic no-apply upgrade plans, dry-run reports, conflict reports,
compatibility reports, migration reports, verification plans, policies,
schemas, commands, tests, golden tasks, docs, export-pack support, and evidence.

Q45 must not upgrade files automatically, overwrite target state, migrate
files, delete files, move files, rewrite references, mutate target
repositories, mutate branches, publish releases, activate CI, or call
providers/models/network.
