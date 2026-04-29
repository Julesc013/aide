# AIDE Hosts

`hosts/` is organized as `vendor / product / adapter-technology`. These directories are future homes for thin host adapters that sit over a shared core.

Exact version coverage does not live in folder names. It belongs in inventory files, matrices, and later manifests. Terminal adapter directories contain placeholder manifests in this phase; implementation is deferred to later prompts.

## Q02 Structural Skeleton

AIDE Hosts are user-facing shells over AIDE Core. Hosts must not own durable semantics, model routing, repo law, workflow semantics, persistent memory, or provider logic.

First-class host categories now have additive skeleton homes:

- `hosts/cli/`: low-friction command host for Harness and future Runtime commands.
- `hosts/service/`: future broker/service host.
- `hosts/commander/`: future desktop command deck for typed repo-native workflows.
- `hosts/extensions/`: future IDE/editor extension host family.
- Mobile remains later/deferred and has no Q02 skeleton.

Existing bootstrap-era proof lanes under `hosts/apple/**`, `hosts/microsoft/**`, `hosts/metrowerks/**`, and `hosts/templates/**` remain in place and are not moved by Q02. Q02 does not implement any host.
