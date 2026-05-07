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
- QFIX-01 is implemented and awaiting review as the foundation reconciliation repair. QFIX-02 AIDE Lite Test Discovery and Runner Fix adds `py -3 .aide/scripts/aide_lite.py test` as the canonical AIDE Lite validation command and is awaiting review.
- Q21 Cross-Repo Pack Export / Import v0 is implemented and awaiting review. It generates `.aide/export/aide-lite-pack-v0/`, validates fixture imports, preserves target `AGENTS.md` manual content, creates target-specific profile and memory templates, and excludes AIDE source identity, queue history, generated context, reports, latest status artifacts, local state, raw prompts, raw responses, and secrets.
- Q24 Existing Tool Adapter Compiler v0 is implemented and awaiting review. It renders compact generated previews for Codex/AGENTS, Claude Code, Aider, Cline, Continue, Cursor, and Windsurf under `.aide/generated/adapters/`, writes only the safe managed `AGENTS.md` section, validates token-survival guidance, and reports drift. It does not implement live tool integrations, provider/model calls, network calls, Gateway forwarding, IDE extensions, or root tool-file overwrites.
- Q22 Eureka and Q23 Dominium pilot evidence now exists in the sibling target repos and awaits target-repo review. The pilots report about 98.6 percent and 99.0 percent estimated task-packet reduction respectively, while preserving the no-source-state/no-secret boundary. AIDE still treats that as target-pilot evidence, not product readiness or proof that every existing-tool adapter output has been exercised.
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
- Q01 documentation split makes the reboot documentation families navigable; it remains documentation-only and stops at review.
- Q02 structural skeleton adds target directories and README ownership boundaries; it remains skeleton-only and stops at review.
- Q03 profile contract defines declarative self-hosting contract records and stops at review.
- Q04 Harness v0 adds a local Python standard-library command surface and stops at review.
- Q05 generated artifacts v0 adds managed downstream outputs and stops at review.
- Q06 Compatibility baseline adds version, migration, replay, upgrade-gate, and deprecation posture; raw status remains `needs_review` while review evidence records `PASS_WITH_NOTES`.
- Q07 Dominium Bridge baseline adds AIDE-side bridge records and structural Harness checks and passed with notes.
- Q08 self-hosting automation adds report-first local checks and passed with notes.
- Q09 through Q20 token-survival foundation layers are accepted with notes by QFIX-01.
- QFIX-01 Foundation Review Reconciliation is implemented and awaiting review.
- QFIX-02 AIDE Lite Test Discovery and Runner Fix is implemented and awaiting review; it keeps the old `-t .` unittest form documented as non-canonical for `.aide/scripts/tests`.
- Q21 Cross-Repo Pack Export / Import v0 is implemented and awaiting review; it is fixture-validated only and does not mutate real Eureka or Dominium repositories.
- Q24 Existing Tool Adapter Compiler v0 is implemented and awaiting review; non-AGENTS tool outputs remain preview-only. Post-pilot evidence from Eureka and Dominium is now available read-only from sibling target repos, but adapter guidance still needs target-tool usage review.
- Current reality: runnable `cli-bridge` proofs exist for selected lanes, while several native lanes remain explicitly blocked or degraded pending real environments, host tooling, or embedded interop work.
- Next likely work: review the Eureka and Dominium import pilots, then run a post-pilot AIDE checkpoint/import-scope refinement before treating adapter guidance as cross-repo-proven.

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
