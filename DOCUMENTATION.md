# AIDE Documentation Index

## Purpose

`DOCUMENTATION.md` is the root guide and index for repository documentation. It defines how documentation should be organized, how authoritative documents relate to each other, and how documentation is kept aligned with reality.

## Documentation Families

- Governance docs define repository law, naming law, support policy, capability doctrine, release policy, and long-term architectural intent.
- Root control-plane docs define current state, contributor guidance, roadmap posture, maintenance posture, planning history, implementation logs, and documentation indexing.
- Self-hosting docs under `.aide/` define the filesystem queue, repo profile, autonomy policy, bypass policy, and review-gate policy for future agent work.
- Constitution docs under `docs/constitution/` freeze baseline repository facts for the reboot.
- Charter docs under `docs/charters/` define bounded reboot goals, public models, internal splits, and non-goals.
- Reference docs under `docs/reference/` explain cross-cutting operational topics that do not belong to a narrower source, governance, or host-lane tree.
- Roadmap docs under `docs/roadmap/` define queue-driven reboot sequencing without adding calendar promises.
- Inventory docs will record exact host families, extension technologies, manifests, and version coverage claims.
- Architecture docs under `specs/` describe shared-core boundaries, host adapter design, interfaces, and cross-cutting technical decisions.
- Boot-slice docs under `specs/boot-slice/` describe the first cross-host implementation target, lane acceptance criteria, degraded or blocked handling, and rollout order.
- Shared contract docs and schemas under `shared/` describe implementation-facing data shapes and subsystem boundaries that must remain aligned with the architecture docs.
- Shared implementation docs and tests under `shared/` describe the executable bootstrap runtime, the CLI bridge, and the deterministic verification layer that now backs the first boot slice.
- Host-lane implementation docs under `hosts/` describe thin lane-local proofs, blocked records, and lane-specific execution-mode choices once host implementation begins.
- Environment docs under `environments/` describe concrete setup models, acquisition posture, bring-up playbooks, snapshots, and machine-readable environment catalogs.
- Lab docs under `labs/` describe experimental, blocked, and archival environment-oriented work that has not yet been promoted into stable control-plane records.
- Evaluation docs under `evals/` describe evaluation models, verification routines, graders, playbooks, result vocabularies, and future run or report records.
- Packaging docs under `packaging/` describe artifact classes, manifest placeholders, release channels, signing posture, packaging checklists, and future release records.
- Maintenance docs under `scripts/maintenance/` describe recurring upkeep tasks, audit checklists, and automation boundaries.
- Repo-local skill docs under `.agents/` describe narrow reusable operational guidance for recurring AIDE work.
- Fixture docs under `fixtures/` describe deterministic requests, responses, and reproducible inputs used by shared-core verification and later host-adapter evals.
- User-facing docs will describe how to use released artifacts, bounded by what is actually shipped.

## Organization Conventions

- Keep authoritative governance material under `governance/`.
- Keep root contributor, roadmap, maintenance, and changelog docs at the repository root.
- Keep the canonical self-hosting queue and policy records under `.aide/`.
- Keep reboot baseline records under `docs/constitution/`.
- Keep reboot goal and model statements under `docs/charters/`.
- Keep reusable explanatory reference docs under `docs/reference/`.
- Keep queue-specific reboot roadmap material under `docs/roadmap/`.
- Keep inventory and matrix material separate from architecture narratives.
- Keep durable product and contract architecture under `specs/architecture/`.
- Keep first-wave implementation targeting, rollout planning, and lane-acceptance specs under `specs/boot-slice/`.
- Keep implementation-facing shared subsystem guides and schemas under `shared/`.
- Keep lane-local host proof artifacts, wrappers, and blocked records inside the corresponding `hosts/<vendor>/<product>/<technology>/` directory.
- Keep shared runtime tests beside the shared runtime under `shared/tests/` and keep deterministic external inputs under `fixtures/`.
- Keep stable environment control-plane docs and catalogs under `environments/`.
- Keep partial or experimental bring-up work under `labs/` until it is ready for promotion.
- Keep evaluation models, machine-readable eval catalogs, and audit playbooks under `evals/`.
- Keep actual verification run records under `evals/runs/` once executable implementation work begins.
- Keep synthesized phase audits and blocker summaries under `evals/reports/`.
- Keep packaging models, machine-readable packaging catalogs, manifest placeholders, and release checklists under `packaging/`.
- Keep reusable maintenance catalogs and checklists under `scripts/maintenance/`.
- Keep narrow operational skills under `.agents/skills/`.
- Keep environment and evaluation evidence close to the systems they verify.
- Prefer small authoritative documents over large mixed-purpose documents.

## Maintenance Conventions

- Documentation must describe reality, not aspiration.
- Update authoritative docs in the same change set that changes the governed behavior or policy.
- If a claim depends on future work, mark it as planned rather than writing it as present fact.
- When a document becomes obsolete, update or supersede it explicitly rather than leaving silent contradictions.

## Current Authoritative Set

- `README.md`: top-level project overview and phase summary.
- `CONTRIBUTING.md`: contributor orientation and scoped-change guidance for human and agentic work.
- `ROADMAP.md`: phase-based roadmap and milestone posture.
- `MAINTENANCE.md`: maintenance domains, sync rules, and automation boundary guidance.
- `CHANGELOG.md`: baseline for future changelog entries without backfilled bootstrap history.
- `AGENTS.md`: root operating law for human contributors and coding agents.
- `PLANS.md`: working plan index for substantial work.
- `IMPLEMENT.md`: engineering execution log.
- `DOCUMENTATION.md`: documentation guide and index.
- `.aide/profile.yaml`: self-hosting repository profile and current reboot focus.
- `.aide/toolchain.lock`: minimal bootstrap harness lock record.
- `.aide/queue/**`: canonical filesystem queue, Q00 task packet, and task evidence.
- `.aide/policies/**`: autonomy, bypass, and review-gate policy records.
- `docs/constitution/bootstrap-era-aide.md`: Q00 baseline freeze for bootstrap-era AIDE.
- `docs/charters/reboot-charter.md`: Q00 charter for the in-place reboot model and non-goals.
- `docs/reference/repo-census.md`: Q00 top-level repository census and conceptual mapping.
- `docs/reference/self-bootstrap.md`: reference guide for the self-bootstrap queue and Q00 prompt.
- `docs/roadmap/reboot-roadmap.md`: queue-driven Q00 through Q08 reboot roadmap.
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
- `hosts/microsoft/**`: first implemented host-lane proof set, including runnable cli-bridge shims, blocked-proof records, and lane-local boot-slice request or response examples.
- `hosts/apple/**`: Apple host-lane proof set, including a runnable companion cli-bridge shim and blocked structural XcodeKit native-proof records.
- `hosts/metrowerks/**`: CodeWarrior host-lane proof set, including a runnable archival-native cli-bridge shim, native-adjacent plug-in target metadata, and a runnable companion fallback proof.
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
- `evals/runs/microsoft-boot-slice-smoke.md`: factual record of the first Microsoft host-lane proof wave, including runnable versus blocked verification boundaries.
- `evals/runs/apple-boot-slice-smoke.md`: factual record of the Apple host-lane proof wave, including runnable companion verification and blocked XcodeKit boundaries.
- `evals/runs/codewarrior-boot-slice-smoke.md`: factual record of the CodeWarrior host-lane proof wave, including runnable archival-native versus companion fallback boundaries.
- `evals/reports/bootstrap-phase-audit.md`: factual post-P13 audit of completed phases, current implementation reality, and next likely work areas.
- `evals/reports/open-blockers-summary.md`: concise blocker rollup across host, environment, packaging, and verification domains.
- `packaging/README.md`: root guide for the packaging and release control plane.
- `packaging/model.md`: canonical packaging model for artifact classes, manifest placeholders, release channels, and signing posture.
- `packaging/catalogs/**`: machine-readable artifact-class, channel, signing-posture, and package-definition catalogs.
- `packaging/checklists/**`: repeatable packaging and release audit procedures.
- `scripts/README.md`: root guide for repeatable repository operations and lightweight automation support.
- `scripts/aide-queue-next`, `scripts/aide-queue-status`, and `scripts/aide-queue-run`: conservative read-only queue helpers.
- `scripts/maintenance/**`: maintenance task catalog, automation boundary, and reusable audit or synchronization checklists.
- `.agents/README.md`: repo-local agent workflow guide.
- `.agents/skills/**`: narrow repo-local skills for recurring inventory, eval, host, maintenance, docs, roadmap, and audit work.

## Current Status

The repository is still pre-product, but it now has governance, inventory, matrices, host-atlas research, shared-core architecture, a defined boot-slice rollout, an executable shared-core bootstrap runtime with deterministic fixtures and tests, the first Microsoft, Apple, and CodeWarrior host-lane proof waves, environment or lab control-plane records, evaluation and packaging control-plane records, contributor or roadmap guidance, maintenance control-plane assets, post-bootstrap audit reports, a minimal self-hosting filesystem queue, and Q00 reboot baseline documents. Broader host-adapter coverage, actual archival environment bring-up, deeper executable eval coverage, packaging automation, shipped artifacts, and real autonomous worker invocation remain future phases.
