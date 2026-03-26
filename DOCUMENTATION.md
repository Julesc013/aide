# AIDE Documentation Index

## Purpose

`DOCUMENTATION.md` is the root guide and index for repository documentation. It defines how documentation should be organized, how authoritative documents relate to each other, and how documentation is kept aligned with reality.

## Documentation Families

- Governance docs define repository law, naming law, support policy, capability doctrine, release policy, and long-term architectural intent.
- Inventory docs will record exact host families, extension technologies, manifests, and version coverage claims.
- Architecture docs under `specs/` describe shared-core boundaries, host adapter design, interfaces, and cross-cutting technical decisions.
- Boot-slice docs under `specs/boot-slice/` describe the first cross-host implementation target, lane acceptance criteria, degraded or blocked handling, and rollout order.
- Shared contract docs and schemas under `shared/` describe implementation-facing data shapes and subsystem boundaries that must remain aligned with the architecture docs.
- Shared implementation docs and tests under `shared/` describe the executable bootstrap runtime, the CLI bridge, and the deterministic verification layer that now backs the first boot slice.
- Environment docs under `environments/` describe concrete setup models, acquisition posture, bring-up playbooks, snapshots, and machine-readable environment catalogs.
- Lab docs under `labs/` describe experimental, blocked, and archival environment-oriented work that has not yet been promoted into stable control-plane records.
- Evaluation docs under `evals/` describe evaluation models, verification routines, graders, playbooks, result vocabularies, and future run or report records.
- Packaging docs under `packaging/` describe artifact classes, manifest placeholders, release channels, signing posture, packaging checklists, and future release records.
- Fixture docs under `fixtures/` describe deterministic requests, responses, and reproducible inputs used by shared-core verification and later host-adapter evals.
- User-facing docs will describe how to use released artifacts, bounded by what is actually shipped.

## Organization Conventions

- Keep authoritative governance material under `governance/`.
- Keep inventory and matrix material separate from architecture narratives.
- Keep durable product and contract architecture under `specs/architecture/`.
- Keep first-wave implementation targeting, rollout planning, and lane-acceptance specs under `specs/boot-slice/`.
- Keep implementation-facing shared subsystem guides and schemas under `shared/`.
- Keep shared runtime tests beside the shared runtime under `shared/tests/` and keep deterministic external inputs under `fixtures/`.
- Keep stable environment control-plane docs and catalogs under `environments/`.
- Keep partial or experimental bring-up work under `labs/` until it is ready for promotion.
- Keep evaluation models, machine-readable eval catalogs, and audit playbooks under `evals/`.
- Keep actual verification run records under `evals/runs/` once executable implementation work begins.
- Keep packaging models, machine-readable packaging catalogs, manifest placeholders, and release checklists under `packaging/`.
- Keep environment and evaluation evidence close to the systems they verify.
- Prefer small authoritative documents over large mixed-purpose documents.

## Maintenance Conventions

- Documentation must describe reality, not aspiration.
- Update authoritative docs in the same change set that changes the governed behavior or policy.
- If a claim depends on future work, mark it as planned rather than writing it as present fact.
- When a document becomes obsolete, update or supersede it explicitly rather than leaving silent contradictions.

## Current Authoritative Set

- `README.md`: top-level project overview and phase summary.
- `AGENTS.md`: root operating law for human contributors and coding agents.
- `PLANS.md`: working plan index for substantial work.
- `IMPLEMENT.md`: engineering execution log.
- `DOCUMENTATION.md`: documentation guide and index.
- `governance/vision.md`: durable project vision and non-goals.
- `governance/support-policy.md`: support tiers, states, modes, and honesty rules.
- `governance/naming-policy.md`: naming doctrine for directories, manifests, adapters, and artifacts.
- `governance/capability-levels.md`: capability levels `L0` through `L4`.
- `governance/release-policy.md`: phase gating and release law.
- `specs/README.md`: root index for architecture and product contracts.
- `specs/architecture/**`: canonical shared-core and host-adapter architecture docs plus ADRs.
- `specs/boot-slice/**`: first-wave implementation target, lane acceptance, rollout, degraded-policy, and machine-readable boot-slice planning manifests.
- `shared/README.md`: root guide for the shared implementation subtree.
- `shared/core/**`, `shared/protocol/**`, `shared/diagnostics/**`, `shared/config/**`, and `shared/cli/**`: executable shared-core bootstrap runtime for the first boot slice.
- `shared/tests/**`: standard-library tests covering the shared-core runtime and CLI smoke path.
- `shared/schemas/**`: conservative machine-readable shared contract shapes that support later implementation.
- `fixtures/boot-slice/**`: deterministic JSON boot-slice requests and expected responses used by tests and smoke verification.
- `environments/README.md`: root guide for the environment control plane.
- `environments/model.md`: canonical model for environment families, instances, media, toolchains, snapshots, bootability, blockers, and archival records.
- `environments/catalogs/**`: machine-readable environment, media, toolchain, snapshot, and bootability catalogs.
- `inventory/legal-acquisition.yaml`: stable acquisition and provenance vocabulary for environment-related assets.
- `labs/README.md`: root guide for active prototypes, blocked work, and archival lab records.
- `labs/workflow.md`: lab progression and promotion guide.
- `labs/**/register.yaml`: machine-readable prototype, blocked, and archival lab registers.
- `evals/README.md`: root guide for the evaluation and verification control plane.
- `evals/model.md`: canonical model for eval categories, verification routines, graders, result states, and evidence posture.
- `evals/catalogs/**`: machine-readable eval, verification, grader, and result-status catalogs.
- `evals/playbooks/**`: repeatable verification and eval procedures.
- `evals/runs/**`: factual records of executable verification runs once implementation exists.
- `packaging/README.md`: root guide for the packaging and release control plane.
- `packaging/model.md`: canonical packaging model for artifact classes, manifest placeholders, release channels, and signing posture.
- `packaging/catalogs/**`: machine-readable artifact-class, channel, signing-posture, and package-definition catalogs.
- `packaging/checklists/**`: repeatable packaging and release audit procedures.

## Current Status

The repository is still pre-product, but it now has governance, inventory, matrices, host-atlas research, shared-core architecture, a defined boot-slice rollout, an executable shared-core bootstrap runtime with deterministic fixtures and tests, environment or lab control-plane records, and evaluation and packaging control-plane records. Host-adapter implementation, actual environment bring-up, broader executable eval coverage, packaging automation, and shipped artifacts remain future phases.
