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
- [docs/reference/apply-lifecycle-schemas.md](docs/reference/apply-lifecycle-schemas.md)
- [docs/reference/aide-lite-release-bundle.md](docs/reference/aide-lite-release-bundle.md)
- [docs/reference/github-release-draft.md](docs/reference/github-release-draft.md)
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
