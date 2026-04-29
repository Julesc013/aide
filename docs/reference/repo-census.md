# Q00 Repository Census

## Purpose

This census records the current top-level repository shape at Q00. It classifies existing areas for the reboot without moving files.

## Root Directories

| Path | Q00 Classification | Reboot Interpretation |
| --- | --- | --- |
| `.agents/` | reinterpret under new model | Agent skills and operational guidance become Control support for queue-driven work. |
| `.aide/` | reinterpret under new model | Canonical self-hosting queue, policies, profile, and task evidence. |
| `.codex/` | keep as bootstrap-era baseline | Codex-local configuration remains useful but is not canonical queue state. |
| `docs/` | reinterpret under new model | Reboot-facing constitution, charters, roadmap, and reference material. |
| `environments/` | keep as bootstrap-era baseline | Environment control plane remains evidence for Compatibility and Harness planning. |
| `evals/` | keep as bootstrap-era baseline | Evaluation records remain historical proof evidence and later Harness input. |
| `fixtures/` | keep as bootstrap-era baseline | Deterministic shared-core inputs remain Harness evidence. |
| `governance/` | keep as bootstrap-era baseline | Repository law remains authoritative unless a future reviewed policy item changes it. |
| `hosts/` | refactor later | Existing host-lane proofs map to AIDE Hosts but are not moved in Q00. |
| `inventory/` | keep as bootstrap-era baseline | Canonical ids and version records remain Compatibility evidence. |
| `labs/` | candidate/deferred | Lab and archival work remains evidence for later environment or Compatibility tasks. |
| `matrices/` | keep as bootstrap-era baseline | Support, capability, feature, platform, packaging, and test posture remain Compatibility and Control evidence. |
| `packaging/` | candidate/deferred | Packaging control plane remains deferred until release evidence matures. |
| `platforms/` | keep as bootstrap-era baseline | Platform notes remain Compatibility context. |
| `research/` | keep as bootstrap-era baseline | Source-backed host research remains input evidence for future planning. |
| `scripts/` | reinterpret under new model | Maintenance and queue helpers become Control and Harness support, not product runtime. |
| `shared/` | refactor later | Existing shared-core boot slice maps toward AIDE Core, but Q00 does not move or split it. |
| `specs/` | keep as bootstrap-era baseline | Architecture and boot-slice specs remain Contract evidence. |

## Root Files

| Path | Q00 Classification | Reboot Interpretation |
| --- | --- | --- |
| `AGENTS.md` | reinterpret under new model | Root operating law now includes the canonical queue rule and review-gated reboot posture. |
| `CHANGELOG.md` | keep as bootstrap-era baseline | Baseline changelog file remains a future release-record aid. |
| `CONTRIBUTING.md` | keep as bootstrap-era baseline | Contributor guidance remains valid unless a future queue item revises it. |
| `DOCUMENTATION.md` | reinterpret under new model | Root documentation index must link reboot documents and preserve prior docs. |
| `IMPLEMENT.md` | reinterpret under new model | Execution log records Q00 and later queue work alongside phase history. |
| `MAINTENANCE.md` | keep as bootstrap-era baseline | Maintenance guidance remains operational baseline. |
| `PLANS.md` | reinterpret under new model | Plan index records Q00 and the queue-driven reboot sequence without deleting P00-P15. |
| `README.md` | reinterpret under new model | Top-level overview acknowledges the reboot while preserving pre-product honesty. |
| `ROADMAP.md` | reinterpret under new model | Root roadmap points to the reboot roadmap and keeps prior phase history. |

## Current-State Map

| Current Structure | Intended Future Conceptual Home | Q00 Action |
| --- | --- | --- |
| `governance/`, `AGENTS.md` | AIDE Core / Control | Preserve and reference. |
| `specs/`, `shared/schemas/` | AIDE Core / Contract | Preserve as bootstrap-era contract evidence. |
| `shared/`, `fixtures/`, `evals/` | AIDE Core / Harness and Compatibility inputs | Preserve; future queue items may refactor. |
| `inventory/`, `matrices/`, `platforms/`, `research/` | AIDE Core / Compatibility | Preserve as source-backed compatibility evidence. |
| `.aide/`, `.agents/`, `scripts/` | AIDE Core / Control and Harness support | Reinterpret for self-hosting workflow. |
| `hosts/` | AIDE Hosts | Preserve proof lanes; refactor later only with evidence. |
| `packaging/` | Candidate release and artifact track | Keep deferred. |
| `environments/`, `labs/` | Compatibility and Harness evidence support | Keep baseline and defer deeper bring-up. |
| Future Dominium Bridge docs and artifacts | AIDE Bridges / Dominium Bridge | Plan through later queue items; do not create implementation in Q00. |

## No-Move Rule

Q00 does not move files, rename directories, split source trees, or rewrite bootstrap-era records. This census is a map for future work, not a structural migration.
