# Bootstrap-Era AIDE Baseline

## Purpose

This document freezes the bootstrap-era baseline for the AIDE reboot. It records what the existing repository achieved before Q00 and preserves that work as history and evidence. The reboot is an in-place refactor of this repository, not a greenfield restart.

## Current Repository Reality

AIDE is an existing, partially implemented, pre-product system. It is operationally structured and has executable proof material in selected areas, but it is not broadly releasable and does not yet provide a finished product surface.

Current implemented reality includes:

- Root operating law, planning records, implementation logs, and documentation indexes.
- Governance, support, naming, capability, and release policy records.
- Inventory and matrix records for host, platform, support, feature, test, and packaging posture.
- Source-backed research records for Microsoft, Apple, CodeWarrior, and broader legacy candidate families.
- Shared-core architecture and boot-slice specifications.
- A deterministic Python standard-library shared-core boot slice with CLI bridge, fixtures, and tests.
- First-wave Microsoft, Apple, and CodeWarrior host-lane proof records, including runnable `cli-bridge` proofs and explicit blocked native records.
- Environment, lab, evaluation, packaging, maintenance, and agent workflow control-plane records.
- The `.aide/queue/` filesystem queue scaffold created by P15.

Future intent includes the reboot model, the Contract, Harness, Compatibility, and Dominium Bridge first shipped stack, and later work on generated artifacts, compatibility baselines, self-hosting automation, Runtime, CLI or Service surfaces, Commander, Mobile, and IDE Hosts. Those are not implemented by Q00.

## Historical Baseline

The P00 through P14 phase history remains authoritative historical baseline:

- `P00`: repository constitution and operating law.
- `P01` through `P05`: inventory, matrices, host-family scaffolding, and source-backed ecosystem atlases.
- `P06`: shared-core architecture and host-adapter contract system.
- `P07`: environment, lab, and acquisition framework.
- `P08`: evaluation, verification, packaging, and release framework.
- `P09`: cross-host boot-slice specification and oldest-first rollout plan.
- `P10`: shared-core boot-slice implementation.
- `P11`: Microsoft host boot-slice proof wave.
- `P12`: Apple host boot-slice proof wave.
- `P13`: CodeWarrior host boot-slice proof wave and backlog stabilization.
- `P14`: documentation normalization, roadmap, contributor guidance, and maintenance automation baseline.

P15 added the self-hosting queue scaffold and Q00 task packet. Q00 uses that scaffold to freeze the baseline; it does not replace P00 through P15.

## Implemented Reality Versus Future Intent

Implemented reality:

- AIDE has a shared-core boot-slice implementation and tests under `shared/`.
- AIDE has host-lane proof artifacts under `hosts/`.
- AIDE has factual eval run records and reports under `evals/`.
- AIDE has planning, documentation, and maintenance control-plane assets.
- AIDE has a filesystem queue scaffold under `.aide/queue/`.

Future intent:

- AIDE Core should be re-expressed around Contract, Harness, Runtime, Compatibility, Control, and SDK.
- The first shipped reboot stack is Contract + Harness + Compatibility + Dominium Bridge.
- Dominium Bridge should be governed by XStack as a strict local governance and proof profile.
- Generated artifacts, profile contracts, compatibility baselines, and self-hosting automation should become reviewable queue-driven outputs.
- Runtime, Commander, Mobile, CLI or Service surfaces, and IDE Hosts remain later tracks until queue evidence supports them.

## Blocked, Deferred, And Incomplete Areas

Known incomplete or deferred areas include:

- No broad release-ready product surface exists.
- Packaging automation, signing, release channels, and shipped artifacts remain incomplete.
- Several native or archival host lanes remain blocked by missing reproducible environments or host tooling.
- Embedded native interop is still blocked or deferred where current proof is `cli-bridge`.
- Environment bring-up and archival media evidence remain incomplete.
- The self-hosting queue exists, but there is no autonomous Codex worker runner.
- Runtime, Commander, Mobile, IDE extension families, provider integrations, and app surfaces are not Q00 scope.

## Preservation Rule

Future reboot work must preserve bootstrap-era documents, phase records, evidence, and blocker history. If later work supersedes an older model, it should add clear mapping and evidence rather than deleting or rewriting the historical record.
