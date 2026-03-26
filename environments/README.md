# AIDE Environments

`environments/` is the control plane for concrete runnable or reconstructable setups used by AIDE.

This area tracks:

- environment families and concrete environment instances
- install media and toolchain references
- snapshot and image references
- bring-up status, bootability, and blockers
- repeatable playbooks for acquisition and bring-up work

This directory is distinct from:

- `platforms/`, which tracks platform-oriented knowledge and cross-platform reference material
- `labs/`, which tracks active experiments, blocked work, and partial bring-up efforts
- `research/`, which tracks source-backed ecosystem facts rather than concrete runnable setups

`environments/` is not a dump of binaries. It exists to record reproducible environment metadata, local-reference expectations, and bring-up structure without checking proprietary media or heavyweight images into Git.
