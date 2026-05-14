# AIDE

Automated Integrated Development Environment.

## Mission

AIDE is a long-horizon engineering repository for a cross-IDE extension and companion platform that spans modern and historical development environments without flattening their differences. It combines source-backed ecosystem research, explicit support metadata, shared-core contracts, thin host adapters, environment tracking, and verification records inside one governed system.

## Core Doctrine

- AIDE is one project with one shared core and many host adapters.
- Source directories are named for compatibility technology or host contract, not exact version ranges.
- Exact version coverage belongs in inventory, manifests, and matrices.
- Support is expressed through support tiers, support states, support modes, and capability levels.
- Different host families may top out at different capability ceilings.

## Current State

- Governance, inventory, matrices, research corpora, architecture docs, environment or lab control-plane records, eval scaffolding, and packaging scaffolding are in place.
- The shared-core boot slice is implemented under `shared/` as a deterministic Python standard-library runtime with CLI bridge, fixtures, and tests.
- First-wave host proofs now exist for Microsoft, Apple, and CodeWarrior lanes, with a mix of runnable `cli-bridge` proofs and explicit blocked or deferred native lanes.
- The self-hosting reboot queue is scaffolded under `.aide/queue/`; it is the canonical route for non-trivial future agent work.
- The self-hosting Profile/Contract v0 is defined under `.aide/` as declarative repo contract data, not Harness execution machinery.
- Q00 adds a baseline freeze and reboot audit that keeps AIDE as an in-place refactor, not a greenfield restart.
- Q01 adds a documentation architecture split around AIDE Core, AIDE Hosts, AIDE Bridges, the internal Core split, and the first shipped stack of Contract + Harness + Compatibility + Dominium Bridge.
- Q02 adds README-only skeleton homes for `core/`, future host categories, and `bridges/`, plus a structural migration map. It does not move the bootstrap-era shared core or host proof lanes.
- Q03 adds the minimal `.aide/` Profile/Contract v0 and source-of-truth references. It does not implement Harness commands, generated artifacts, Runtime, Hosts, Bridges, provider adapters, or app surfaces.
- Q04 adds the minimal executable Harness v0 at `scripts/aide` with structural validation, doctoring, compile-plan, migration-baseline, and bakeoff-readiness reports. It does not generate downstream artifacts.
- Q05 adds generated artifacts v0: deterministic managed sections, a preview-only Claude guidance artifact, a generated manifest, and Harness drift checks. Generated artifacts are not canonical truth.
- Q06 adds the Compatibility baseline: known v0 version records, a no-op migration registry, structural replay metadata, upgrade gates, deprecation record format, and Harness validate/migrate checks. It does not implement real migrations or Dominium Bridge behavior.
- Q07 adds the AIDE-side Dominium Bridge baseline: bridge metadata, XStack boundary records, a profile overlay, strict policy overlays, generated target expectations, compatibility pinning, and structural Harness checks. It does not modify the Dominium repo or emit real Dominium outputs.
- Q08 adds report-first self-hosting automation scaffolding: `aide self-check`, non-canonical self-check reports, clearer queue-runner output, and doctor next-step cleanup. It passed review with notes and does not invoke external agents, refresh generated artifacts, or create Runtime/Service/Commander behavior.
- Q09 through Q20 are accepted with notes by QFIX-01 as the token-survival foundation: compact task/context/review packets, deterministic verifier and golden-task gates, estimated token ledger, advisory outcome and routing reports, cache/local-state boundaries, local/report-only Gateway skeleton, and offline provider metadata. These layers reduce AIDE queue prompt surfaces and preserve local substrate quality gates, but they do not prove arbitrary coding-task quality or product readiness.
- Q19 Gateway and Q20 provider surfaces remain no-call/report-only or offline metadata only. They do not implement OpenAI/Anthropic-compatible forwarding, provider/model calls, credential setup, Runtime, Service, Commander, UI, Mobile, MCP/A2A, or autonomous execution.
- QFIX-01 and QFIX-02 are accepted with notes by QFIX-03 as foundation reconciliation and validation-runner truth repair. QFIX-02 establishes `py -3 .aide/scripts/aide_lite.py test` as the canonical AIDE Lite validation command.
- Q21 Cross-Repo Pack Export / Import v0 is accepted with notes by QFIX-03. It generates `.aide/export/aide-lite-pack-v0/`, validates fixture imports, preserves target `AGENTS.md` manual content, creates target-specific profile and memory templates, and excludes AIDE source identity, queue history, generated context, reports, latest status artifacts, local state, raw prompts, raw responses, and secrets.
- Q24 Existing Tool Adapter Compiler v0 is accepted with notes by QFIX-03. It renders compact generated previews for Codex/AGENTS, Claude Code, Aider, Cline, Continue, Cursor, and Windsurf under `.aide/generated/adapters/`, writes only the safe managed `AGENTS.md` section, validates token-survival guidance, and reports drift. It does not implement live tool integrations, provider/model calls, network calls, Gateway forwarding, IDE extensions, or root tool-file overwrites.
- Q22 Eureka and Q23 Dominium pilot evidence now exists in the sibling target repos and awaits target-repo review. The pilots report about 98.6 percent and 99.0 percent estimated task-packet reduction respectively, while preserving the no-source-state/no-secret boundary. AIDE still treats that as target-pilot evidence, not product readiness or proof that every existing-tool adapter output has been exercised.
- Q25 through Q31 are accepted with notes by QFIX-03 as AIDE governance, pack/import, handover, commit discipline, WorkUnit recovery, Git workflow, dry-run helper, branch-policy, and export-pack sync work. They do not imply product readiness, live branch mutation, target-repo mutation, provider/model calls, or release automation.
- Q34 Changelog and Release Notes Generator v0 is accepted with notes by QFIX-03. It compiles structured commits into preview-only changelog and release-note Markdown/JSON drafts, reports malformed history for review, adds Q34 golden tasks and tests, and keeps tags, GitHub Releases, branch mutation, and publishing deferred.
- Q35 GitHub Protection and CI Advisory v0 adds report-only GitHub branch-protection and CI gate advisory policies, `.aide/github` generated reports, AIDE Lite `github` commands, tests, golden tasks, docs, and export-pack support. It does not call GitHub APIs, create `.github/workflows`, mutate branches, create tags, publish releases, or call providers/models/network.
- Q36 Intent Compiler and Prompt Normalization v0 adds deterministic, no-call prompt classification and WorkUnit draft generation under `.aide/intake/`. It normalizes vague, overbroad, destructive, Git, release, install, and repair prompts into bounded reviewable intent packets without executing the resulting task.
- Q37 Repo Intelligence Index v0 adds deterministic, no-call file inventory, ownership, dependency, test, documentation-link, generated-output, and orphan-candidate indexes under `.aide/repo/`. It classifies repo state for future WorkUnits without moving, deleting, rewriting, or judging files as dead.
- Q38 File Quality Ledger v0 adds deterministic, no-call advisory quality reports under `.aide/reports/`. It measures ownership, docs, tests, validators, stale docs, generated/evidence boundaries, orphan candidates, module-size hints, and reuse candidates without moving, deleting, refactoring, or auto-fixing files.
- Q39 Refactor Control Plane v0 adds deterministic, no-call dry-run planning under `.aide/refactors/`. It defines refactor, migration, move-map, salvage-map, path-alias, rollback-note, and migration-ledger schemas plus `refactor` commands without applying moves, deletes, rewrites, migrations, or target-repo mutations.
- Q40 Root Recycling Framework v0 adds deterministic, no-call root inventory, root classification, per-file fate candidates, root risk summaries, exception records, and no-apply `roots` plans under `.aide/roots/`. It does not move roots, delete files, rewrite references, absorb tools, or classify anything as safe to delete.
- Q41 Existing Tool Absorption v0 adds deterministic, no-call tool inventory, capability classification, preservation fates, risk summaries, adapter maps, and no-execution `tools` wrap plans under `.aide/tools/`. It does not execute unknown tools, delete, rename, migrate, replace, or actively wrap existing tool systems.
- Q42 Move Map / Salvage Map / Path Alias v0 adds deterministic, no-call candidate move maps, salvage maps, path alias plans, reference rewrite plans, and draft migration ledger events under `.aide/refactors/`. It does not move files, delete files, rewrite references, create aliases or shims, apply maps, or treat candidate maps as approved migration truth.
- Q43 Install Plan Model v0 adds deterministic, no-call install observation, candidate install plans, dry-run reports, ownership ledgers, conflict reports, preservation reports, and verification plans under `.aide/install/`. It does not install, overwrite, migrate, delete, move, rewrite, mutate target repos, or treat source-generated state as target truth.
- Q44 Repair / Doctor Model v0 adds deterministic, no-call repair observation, diagnosis, candidate repair plans, dry-run reports, doctor repair reports, and verification plans under `.aide/repair/`. It does not repair, overwrite, delete, migrate, move, rewrite, install, mutate target repos, or treat repair findings as apply approval.
- Q45 Upgrade Model v0 adds deterministic, no-call current-install observation, source-pack observation, compatibility comparison, candidate upgrade plans, dry-run reports, conflict reports, migration reports, and verification plans under `.aide/upgrade/`. It does not upgrade, overwrite, delete, migrate, install, repair, move, rewrite, mutate target repos, or treat dry-run output as apply approval.
- Q46 Rollback / Uninstall Model v0 adds deterministic, no-call rollback and uninstall observations, preservation-first plans, dry-run reports, and verification plans under `.aide/rollback/` and `.aide/uninstall/`. It does not roll back, uninstall, delete, overwrite, remove managed sections, mutate target repos, or treat unknown ownership as removable.
- Q47 AIDE Lite Release Bundle v0 adds deterministic, local-only release bundle generation under `.aide/release/` and `.aide/release/dist/`. It creates inspectable `.zip` and `.tar.gz` archives, checksums, manifests, install notes, provenance, and extraction validation from the validated export pack, but it does not publish, upload, tag, create GitHub Releases, mutate branches, or install into target repos.
- The repository remains pre-product. Packaging, release automation, deeper native verification, and broader environment bring-up are still incomplete.

## Repository Map

- `.aide/`: self-hosting Profile/Contract v0, filesystem queue, and autonomy or review-gate policies
- `core/`: README-only target skeleton for AIDE Core bands; current implementation remains under `shared/`
- `bridges/`: AIDE Bridges, starting with the Q07 Dominium Bridge baseline
- `governance/`: repository law, support policy, naming law, capability doctrine, and release policy
- `inventory/`: canonical ids, version records, and machine-readable support inputs
- `matrices/`: support, capability, feature, verification, packaging, and platform posture by lane
- `docs/`: reboot constitution, architecture charters, roadmaps, decisions, design-mining indexes, and operational references
- `research/`: source-backed ecosystem atlases and unresolved-item registers
- `specs/`: architecture contracts and boot-slice specifications
- `shared/`: shared-core implementation, schemas, CLI bridge, and tests
- `hosts/`: bootstrap-era host-lane proofs plus README-only skeletons for CLI, Service, Commander, and extension host categories
- `environments/`: concrete environment control plane and bring-up catalogs
- `labs/`: prototype, blocked, and archival environment-oriented work
- `evals/`: verification models, run records, and audit reports
- `packaging/`: packaging and release-shape control plane
- `scripts/`: repeatable repository maintenance assets and future lightweight automation support
- `.agents/`: repo-local skills and operational guidance for agentic work

## Phase Status

- Completed bootstrap phases: P00 through P09 established governance, research, architecture, environment, evaluation, packaging, and boot-slice planning.
- Completed implementation phases: P10 through P13 delivered the shared-core boot slice plus first Microsoft, Apple, and CodeWarrior host-family proof waves.
- Self-bootstrap phase P15 adds a queue scaffold and first Q00 ExecPlan for future filesystem-driven work; it does not implement later queue items.
- Q01 documentation split, Q02 structural skeleton, and Q03 profile contract are accepted with notes by QFIX-03. They remain documentation, skeleton, and declarative contract work only.
- Q04 Harness v0 adds a local Python standard-library command surface and stops at review.
- Q05 generated artifacts v0 and Q06 Compatibility baseline are accepted with notes by QFIX-03. Generated outputs remain non-canonical and compatibility work remains metadata/no-op migration posture only.
- Q07 Dominium Bridge baseline adds AIDE-side bridge records and structural Harness checks and passed with notes.
- Q08 self-hosting automation adds report-first local checks and passed with notes.
- Q09 through Q20 token-survival foundation layers are accepted with notes by QFIX-01.
- QFIX-01, QFIX-02, Q21, Q24, Q25, Q26, Q27, Q28, Q29, Q30, Q31, Q34, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q42, Q43, Q44, Q45, Q46, and Q47 are accepted, implemented, or review-gated with explicit no-mutation limits. Their limits remain in force: no raw prompt execution, product readiness, target-repo mutation, live branch mutation, provider/model calls, active CI, GitHub API mutation, release publishing, tags, file moves/deletes, root moves/deletes, reference rewrites, alias/shim application, tool deletion/rename/migration/execution, install apply, repair apply, upgrade apply, rollback apply, uninstall apply, managed-section removal, overwrites, auto-fixes, uploads, or GitHub Releases.
- Current reality: runnable `cli-bridge` proofs exist for selected lanes, while several native lanes remain explicitly blocked or degraded pending real environments, host tooling, or embedded interop work.
- Next AIDE-local work: Q48 GitHub Release Draft v0, using the Q47 local bundle evidence without creating a tag, upload, publication, or active GitHub Release. Target-side Q32/Q33 sync evidence exists in sibling repos and remains target-local.

## Key Documents

- [AGENTS.md](AGENTS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ROADMAP.md](ROADMAP.md)
- [MAINTENANCE.md](MAINTENANCE.md)
- [PLANS.md](PLANS.md)
- [IMPLEMENT.md](IMPLEMENT.md)
- [DOCUMENTATION.md](DOCUMENTATION.md)
- [.aide/profile.yaml](.aide/profile.yaml)
- [.aide/toolchain.lock](.aide/toolchain.lock)
- [core/README.md](core/README.md)
- [core/contract/README.md](core/contract/README.md)
- [core/harness/README.md](core/harness/README.md)
- [docs/reference/harness-v0.md](docs/reference/harness-v0.md)
- [docs/reference/generated-artifacts-v0.md](docs/reference/generated-artifacts-v0.md)
- [docs/reference/compatibility-baseline.md](docs/reference/compatibility-baseline.md)
- [docs/reference/dominium-bridge.md](docs/reference/dominium-bridge.md)
- [docs/reference/self-hosting-automation.md](docs/reference/self-hosting-automation.md)
- [docs/reference/token-survival-core.md](docs/reference/token-survival-core.md)
- [docs/reference/aide-lite.md](docs/reference/aide-lite.md)
- [docs/reference/aide-lite-test-runner.md](docs/reference/aide-lite-test-runner.md)
- [docs/reference/context-compiler-v0.md](docs/reference/context-compiler-v0.md)
- [docs/reference/verifier-v0.md](docs/reference/verifier-v0.md)
- [docs/reference/evidence-review-workflow.md](docs/reference/evidence-review-workflow.md)
- [docs/reference/token-ledger.md](docs/reference/token-ledger.md)
- [docs/reference/golden-tasks-v0.md](docs/reference/golden-tasks-v0.md)
- [docs/reference/outcome-controller-v0.md](docs/reference/outcome-controller-v0.md)
- [docs/reference/router-profile-v0.md](docs/reference/router-profile-v0.md)
- [docs/reference/cache-local-state-boundary.md](docs/reference/cache-local-state-boundary.md)
- [docs/reference/gateway-skeleton.md](docs/reference/gateway-skeleton.md)
- [docs/reference/provider-adapter-v0.md](docs/reference/provider-adapter-v0.md)
- [docs/reference/cross-repo-pack-export-import.md](docs/reference/cross-repo-pack-export-import.md)
- [docs/reference/existing-tool-adapter-compiler-v0.md](docs/reference/existing-tool-adapter-compiler-v0.md)
- [docs/reference/commit-discipline.md](docs/reference/commit-discipline.md)
- [docs/reference/workunit-idempotency.md](docs/reference/workunit-idempotency.md)
- [docs/reference/changelog-preview.md](docs/reference/changelog-preview.md)
- [docs/reference/github-protection-ci-advisory.md](docs/reference/github-protection-ci-advisory.md)
- [docs/reference/intent-compiler.md](docs/reference/intent-compiler.md)
- [docs/reference/repo-intelligence-index.md](docs/reference/repo-intelligence-index.md)
- [docs/reference/file-quality-ledger.md](docs/reference/file-quality-ledger.md)
- [docs/reference/refactor-control-plane.md](docs/reference/refactor-control-plane.md)
- [docs/reference/root-recycling-framework.md](docs/reference/root-recycling-framework.md)
- [docs/reference/tool-absorption.md](docs/reference/tool-absorption.md)
- [docs/reference/move-salvage-path-aliases.md](docs/reference/move-salvage-path-aliases.md)
- [docs/reference/aide-install-model.md](docs/reference/aide-install-model.md)
- [docs/reference/aide-repair-model.md](docs/reference/aide-repair-model.md)
- [docs/reference/aide-upgrade-model.md](docs/reference/aide-upgrade-model.md)
- [docs/reference/aide-rollback-uninstall.md](docs/reference/aide-rollback-uninstall.md)
- [docs/reference/aide-lite-release-bundle.md](docs/reference/aide-lite-release-bundle.md)
- [docs/reference/git-workflow-policy.md](docs/reference/git-workflow-policy.md)
- [docs/reference/branch-roles.md](docs/reference/branch-roles.md)
- [docs/reference/promotion-policy.md](docs/reference/promotion-policy.md)
- [docs/reference/git-helper-workflow.md](docs/reference/git-helper-workflow.md)
- [docs/reference/aide-dev-main-workflow.md](docs/reference/aide-dev-main-workflow.md)
- [.aide/queue/QCHECK-token-survival-foundation-audit/audit-report.md](.aide/queue/QCHECK-token-survival-foundation-audit/audit-report.md)
- [.aide/queue/QFIX-01-foundation-review-reconciliation/evidence/reconciliation-report.md](.aide/queue/QFIX-01-foundation-review-reconciliation/evidence/reconciliation-report.md)
- [.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/test-runner-fix.md](.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/test-runner-fix.md)
- [.aide/generated/manifest.yaml](.aide/generated/manifest.yaml)
- [hosts/README.md](hosts/README.md)
- [bridges/README.md](bridges/README.md)
- [docs/constitution/README.md](docs/constitution/README.md)
- [docs/constitution/bootstrap-era-aide.md](docs/constitution/bootstrap-era-aide.md)
- [docs/constitution/reboot-doctrine.md](docs/constitution/reboot-doctrine.md)
- [docs/charters/README.md](docs/charters/README.md)
- [docs/charters/reboot-charter.md](docs/charters/reboot-charter.md)
- [docs/charters/core-charter.md](docs/charters/core-charter.md)
- [docs/charters/contract-charter.md](docs/charters/contract-charter.md)
- [docs/charters/harness-charter.md](docs/charters/harness-charter.md)
- [docs/charters/compatibility-charter.md](docs/charters/compatibility-charter.md)
- [docs/charters/hosts-charter.md](docs/charters/hosts-charter.md)
- [docs/charters/bridges-charter.md](docs/charters/bridges-charter.md)
- [docs/charters/control-charter.md](docs/charters/control-charter.md)
- [docs/charters/sdk-charter.md](docs/charters/sdk-charter.md)
- [docs/reference/README.md](docs/reference/README.md)
- [docs/reference/profile-contract-v0.md](docs/reference/profile-contract-v0.md)
- [docs/reference/source-of-truth.md](docs/reference/source-of-truth.md)
- [docs/reference/repo-census.md](docs/reference/repo-census.md)
- [docs/reference/documentation-migration-map.md](docs/reference/documentation-migration-map.md)
- [docs/reference/structural-migration-map.md](docs/reference/structural-migration-map.md)
- [docs/reference/terminology.md](docs/reference/terminology.md)
- [docs/roadmap/README.md](docs/roadmap/README.md)
- [docs/roadmap/reboot-roadmap.md](docs/roadmap/reboot-roadmap.md)
- [docs/roadmap/queue-roadmap.md](docs/roadmap/queue-roadmap.md)
- [docs/roadmap/staged-expansion-roadmap.md](docs/roadmap/staged-expansion-roadmap.md)
- [docs/reference/self-bootstrap.md](docs/reference/self-bootstrap.md)
- [docs/decisions/README.md](docs/decisions/README.md)
- [docs/design-mining/README.md](docs/design-mining/README.md)

## Status Boundary

This repository is operationally structured and partially implemented, but it is not broadly releasable. Blocked, deferred, degraded, and candidate areas remain explicit by design.
