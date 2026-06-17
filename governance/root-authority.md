# Root Authority

## Purpose

This document defines AIDE's current human-readable root authority contract.
It converts the Track B structure audit into repository law without applying a
filesystem migration.

Machine-readable root authority records live in
`.aide/policies/root-authority.yaml`.

## Core Rule

Root classification is not move authority.

A root authority contract explains what a root is allowed to mean. It does not
move files, delete files, rewrite references, create aliases, create shims,
create new top-level roots, or approve generated outputs as source truth.

## Authority Layers

`.aide/` is the repo-local AIDE control-plane root. It owns the Profile,
machine policies, queue, protocol schemas, evidence, generated reports, and OKF
projections. Generated reports and projections inside `.aide/` are evidence or
views unless a later reviewed policy explicitly makes a narrower artifact
canonical.

`core/` is implementation library code. It can implement helpers and validators
for protocol objects, knowledge, reconciler, conformance, patching, adapters,
context, interop, and future runtime surfaces. It does not own queue state.

`governance/` is human-readable law and doctrine. Machine-readable law belongs
under `.aide/policies/`.

`docs/` explains repository behavior and records planning, references,
operations, decisions, and roadmap posture. Docs do not override the Profile,
queue, machine policies, protocol schemas, evidence, or generated-output
boundaries.

`inventory/` records observed facts. `matrices/` records cross-cutting views.
Neither root may fabricate support, capability, compatibility, or release
claims.

`hosts/` contains host integrations or host-lane proofs. `bridges/` contains
target-repo bridge metadata and adoption expectations. AIDE-side bridge records
do not mutate target repositories.

`shared/`, `platforms/`, `research/`, and `specs/` remain preserved
bootstrap-era or unresolved material until a reviewed fate map assigns their
future posture.

`.agents/` and `.codex/` are dot-tool interop/projection surfaces. They are not
hidden queue, protocol, evidence, or policy truth.

`labs/` is experimental. Promotion out of labs requires a queue item and
evidence.

## Generated Outputs

Generated downstream artifacts remain outputs. Examples include `.aide/reports`,
`.aide/repo`, `.aide/roots`, `.aide/refactors`, `.aide/tools`, `.aide/install`,
`.aide/repair`, `.aide/upgrade`, `.aide/rollback`, `.aide/uninstall`, and
`.aide/release`.

These outputs can be evidence. They are not canonical source truth unless a
later reviewed policy explicitly marks a specific artifact as canonical.

## Structural Changes

Future structural changes require all of the following:

1. A queue item with explicit allowed paths and forbidden operations.
2. Current repo/root/refactor evidence.
3. A no-apply map that names candidate moves, salvage, aliases, rewrites, and
   validation needs.
4. A review gate before any apply-capable task.
5. Validation and rollback evidence appropriate to the change.

`drop_candidate`, `archive`, `alias`, `shim`, and `rewrite` remain candidate
language until a future reviewed apply phase says otherwise.

## Review Boundary

This root authority contract stops at review. It does not authorize:

- file moves;
- file deletes;
- reference rewrites;
- path aliases or shims;
- new top-level roots;
- generated-output source-truth promotion;
- branch mutation;
- target-repo mutation;
- provider/model calls;
- network calls;
- release or publishing actions;
- runtime, worker, host, provider, Commander, Workbench, or Service work.
