# Root Authority Contracts

`AIDE-STRUCTURE-01-root-authority-contracts` converts the Track B audit into a
reviewable contract layer.

## What Changed

- Added `.aide/policies/root-authority.yaml` for machine-readable root
  authority classification.
- Added `governance/root-authority.md` for human-readable root law.
- Added `docs/reference/repository-layout.md` for the current closed root model,
  overlap report, candidate target structure, migration rules, validation plan,
  and follow-up prompts.
- Added `.aide/reports/root-authority-contracts.*` as task evidence.

## Root Model

The current model keeps the existing roots in place. It assigns meaning before
movement and keeps unresolved roots behind fate maps:

- `.aide` remains the AIDE control-plane root.
- `core` remains reusable implementation library code.
- `governance` and `.aide/policies` split human law from machine policy.
- `docs` explains but does not override profile, queue, policy, protocol, or
  evidence truth.
- `shared`, `platforms`, `research`, and `specs` need fate maps.
- `.agents` and `.codex` need dot-tool interop policy.
- `tools`, `tests`, `examples`, and `archive` remain add-only candidates.

## Non-Authorization

This task does not authorize file moves, file deletes, reference rewrites, path
aliases, shims, new top-level roots, generated-output source-truth promotion,
branch mutation, target-repo mutation, provider/model calls, network calls,
release work, or Track A protocol implementation.

## Next

The next Track B task should be `AIDE-STRUCTURE-02-status-doc-sync` unless live
queue truth or a review gate selects a narrower prerequisite.
