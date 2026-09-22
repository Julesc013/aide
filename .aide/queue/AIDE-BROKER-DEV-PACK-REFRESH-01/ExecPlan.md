# ExecPlan: Post-Integration Portable Artifact Refresh

## Objective

Return `dev` to a self-consistent portable-artifact state after the broker
runtime integration changed tracked export inputs.

## Scope

This task owns local regeneration of `.aide/export/aide-lite-pack-v0/**`, local
release outputs under `.aide/release/**`, its task evidence, and the narrow
parent closeout records. Runtime source, configuration, publication, tags,
GitHub mutation, and target repositories are outside scope.

## Progress

- [x] Observe the post-landing validation failure and exact manifest source.
- [x] Compile the broad intent and split out this non-publishing local slice.
- [x] Create an isolated task branch and worktree from published dev.
- [x] Admit the bounded local artifact refresh.
- [ ] Commit and publish the admission checkpoint.
- [ ] Regenerate the portable export pack from a clean source commit.
- [ ] Regenerate the local release bundle from the refreshed export pack.
- [ ] Run pack, release, consumer, doctor, and canonical validation.
- [ ] Commit and publish exact refreshed artifacts and evidence.
- [ ] Land through dev, observe refs, and close the parent integration task.

## Verification

- Compare generated path scope against the task allowlist.
- Run `pack-status`, `release validate`, and applicable manifest/checksum views.
- Run `test_export_import.py` and `test_q47_release_bundle.py`.
- Run `doctor`, `validate`, and commit checks.
- Record all skips, failures, and retained publication gates honestly.

## Recovery

Before artifact commit, discard only generator-owned output from this isolated
task worktree and regenerate. After publication, fix forward. Never use these
local artifacts as proof of a public GitHub Release.
