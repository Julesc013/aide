# AIDE Full Audit Repo Map

Date: 2026-04-29

## Root Files

| Path | Current Purpose | Future Conceptual Home | Status |
| --- | --- | --- | --- |
| `AGENTS.md` | Root operating law for agents. | Control guidance over queue and Profile/Contract use. | implemented, maintained |
| `README.md` | Human repo overview and reboot pointers. | Root overview into docs and queue. | partial, slightly stale around Q04 planning |
| `ROADMAP.md` | Root phase and reboot roadmap pointer. | Roadmap index; detailed reboot roadmap lives under `docs/roadmap/`. | partial |
| `PLANS.md` | Working plan index. | Control/planning record. | implemented, historical plus reboot entries |
| `IMPLEMENT.md` | Engineering execution log. | Control/evidence record. | implemented, historical plus reboot entries |
| `DOCUMENTATION.md` | Root documentation index. | Documentation control index. | implemented, updated through Q03 |
| `CONTRIBUTING.md` | Contributor workflow and verification guidance. | Contributor control guidance. | bootstrap-era baseline |
| `MAINTENANCE.md` | Maintenance task and evidence guidance. | Control/maintenance reference. | bootstrap-era baseline |
| `CHANGELOG.md` | Release/history placeholder. | Release record when releases exist. | minimal, pre-product |

## Top-Level Directories

| Directory | Current Purpose | Future Conceptual Home | Status |
| --- | --- | --- | --- |
| `.aide/` | Canonical Profile/Contract records, queue, policy, evidence. | AIDE self-hosting contract and execution source. | partial, implemented through Q03 |
| `.agents/` | Repo-local skills, templates, and agent guidance. | Control support and future generated/maintained agent guidance. | implemented guidance, not generated target output |
| `.codex/` | Local Codex/session tooling directory. | Not canonical AIDE source. | local/tooling, not part of reboot contract |
| `docs/` | Reboot documentation families and references. | Durable documentation surface. | partial, navigable |
| `core/` | README-only reboot Core skeleton. | AIDE Core: Contract, Harness, Runtime, Compatibility, Control, SDK. | skeleton |
| `core/contract/` | Contract docs and v0 shape references. | AIDE Core Contract. | partial |
| `core/harness/` | Harness skeleton README only. | Future executable Harness v0. | skeleton, Q04 pending |
| `core/runtime/` | Runtime placeholder. | Future Runtime substrate. | deferred |
| `core/compat/` | Compatibility skeleton README. | Compatibility baseline and migrations. | skeleton, Q06 deferred |
| `core/control/` | Control skeleton README. | Future control records and policy validation. | skeleton |
| `core/sdk/` | SDK skeleton README. | Future SDK surfaces. | deferred |
| `core/tests/` | Cross-Core test placeholder. | Future Core test home. | skeleton |
| `shared/` | Bootstrap-era shared-core implementation, schemas, CLI bridge, tests. | Future mappings into Core areas if reviewed. | implemented bootstrap-era baseline |
| `hosts/` | Bootstrap-era host proof lanes plus Q02 host-category skeletons. | AIDE Hosts. | partial, mixed historical evidence and skeleton |
| `bridges/` | Q02 bridge skeleton. | AIDE Bridges. | skeleton |
| `bridges/dominium/` | Dominium Bridge and XStack placeholder homes. | First intended bridge baseline. | skeleton, Q07 deferred |
| `governance/` | Support, capability, naming, and repo law. | Control and constitution inputs. | implemented bootstrap-era baseline |
| `inventory/` | Host/platform ids and version records. | Compatibility and Control inputs. | implemented bootstrap-era baseline |
| `matrices/` | Support, capability, feature, platform, test, and packaging matrices. | Compatibility and Control inputs. | implemented bootstrap-era baseline |
| `research/` | Source-backed ecosystem research. | Compatibility and design-mining inputs. | historical evidence |
| `specs/` | Bootstrap-era architecture and boot-slice specs. | Contract and historical architecture evidence. | historical evidence |
| `environments/` | Environment and lab control-plane records. | Control and Compatibility inputs. | partial |
| `labs/` | Lab/prototype/blocker records. | Lab and proof evidence input. | partial |
| `evals/` | Eval declarations and reports. | Harness, Compatibility, and Control inputs. | partial bootstrap-era evidence |
| `packaging/` | Packaging placeholders and release-shape records. | Deferred release/artifact control area. | partial, deferred |
| `scripts/` | Queue helper scripts and maintenance notes. | Future Harness/CLI support where reviewed. | partial; queue helpers implemented, Harness absent |
| `fixtures/` | Bootstrap-era fixtures for shared-core proof work. | Future tests/Harness inputs if migrated. | implemented bootstrap-era baseline |
| `platforms/` | Platform records. | Compatibility inputs. | bootstrap-era baseline |

## Bootstrap-Era Versus Reboot-Era

Bootstrap-era directories remain physically in place and should be treated as evidence and compatibility input. Reboot-era skeletons do not supersede or relocate those files.

Reboot-era structure currently means documentation, contract declarations, queue packets, and README-only skeletons. It does not yet mean executable Harness, Runtime, generated artifacts, or Dominium Bridge implementation.
