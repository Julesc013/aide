# AIDE

Automated Integrated Development Environment ("aid")

## Mission

AIDE is a long-horizon engineering repository for building a cross-IDE extension and companion platform that can operate across modern and historical development environments without flattening their differences. The project exists to produce reusable automation, explicit support metadata, and disciplined host integrations that can be verified honestly over time.

## Long-Horizon Scope

AIDE is intentionally cross-IDE and cross-era. It is expected to span multiple host families as feasible, including modern and historical environments, while accepting that different hosts expose different extension surfaces, automation hooks, and practical ceilings. Scope expansion is governed by inventory, matrices, and verification rather than by broad compatibility claims.

## Architectural Doctrine

AIDE is one project with one shared core and many host adapters. The shared core is where reusable logic, metadata handling, protocols, and cross-host behavior belong. Host adapters translate that core into the extension, SDK, or companion model exposed by a specific host family or compatibility technology.

## Naming And Coverage Doctrine

Source directories are named for compatibility technology or host contract, not version ranges. Exact version coverage belongs in metadata/manifests, inventory records, and support matrices rather than in architectural folder names.

## Support Model

AIDE does not use vague supported or unsupported language as its primary contract. Support is expressed through support tiers and capability levels. A support tier states maintenance and release intent. A capability level states the deepest verified integration depth for a host lane. Different hosts may top out at different levels.

## Planned Repository Map

- `governance/`: repository constitution, support law, naming law, capability model, and release policy.
- `inventory/`: planned machine-readable catalog of host families, extension technologies, and exact coverage claims.
- `matrices/`: planned support and capability views derived from inventory data.
- `shared/`: planned shared core logic that can be reused across host adapters.
- `hosts/`: planned host-family and contract-specific adapter source trees.
- `environments/`: planned reproducible execution and verification environments.
- `labs/`: planned bounded experiments and research prototypes that are not yet product lanes.
- `evals/`: planned evaluation records, verification outputs, and evidence for claimed behavior.
- `packaging/`: planned release assembly logic and artifact definitions.
- `.agents/`: planned Codex and automation harness material for long-horizon human plus agentic development.

## Current Status

This repository is in governance/bootstrap phase. The current work defines operating law, naming doctrine, support doctrine, capability doctrine, and release gates. Product implementation, host adapters, inventory systems, and packaging are intentionally deferred.

## What Comes Next

Later prompts will build the inventory and matrix system, repository scaffolding, Codex harness material, and only then begin implementation work for shared-core and adapter lanes.
