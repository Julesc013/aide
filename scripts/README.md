# AIDE Scripts

`scripts/` holds repeatable repository operations and lightweight automation support for AIDE.

This area is distinct from:

- `.agents/skills/`, which holds narrow reusable instructions for agentic work
- `shared/`, which holds product-facing shared-core implementation
- `hosts/`, which holds host-lane proofs and adapter-local artifacts

This phase establishes a maintenance baseline under `scripts/maintenance/`. It does not create a full automation system or CI pipeline.

Use `scripts/` for:

- repeatable repository audits
- maintenance task catalogs
- checklist or runbook assets that support future automation

Do not use `scripts/` as a dump for speculative tooling or product features.
