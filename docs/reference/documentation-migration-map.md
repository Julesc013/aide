# Documentation Migration Map

## Purpose

This map explains how current and bootstrap-era documentation areas relate to the Q01 documentation families. Q01 does not move files. It links, reinterprets, and preserves old records.

## Map

| Current Area | Q01 Family Or Conceptual Home | Q01 Action |
| --- | --- | --- |
| `README.md` | Root overview plus links to `docs/constitution/`, `docs/charters/`, `docs/roadmap/`, and `docs/reference/` | Update pointers only; preserve pre-product honesty. |
| `DOCUMENTATION.md` | Root documentation index | Add Q01 families and authoritative records. |
| `ROADMAP.md` | Root phase roadmap | Link reboot, queue, and staged expansion roadmaps. |
| `PLANS.md` | Root plan index | Add Q01 implementation entry without removing P00-P15 or Q00 history. |
| `IMPLEMENT.md` | Root execution log | Add Q01 execution record. |
| `governance/**` | Constitution and Control inputs | Preserve as bootstrap-era law unless a future review-gated policy item changes it. |
| `specs/**` | Contract and bootstrap-era architecture evidence | Preserve as existing architecture and boot-slice records; do not move in Q01. |
| `research/**` | Compatibility and design-mining inputs | Preserve as source-backed ecosystem research; later design-mining may cite it. |
| `evals/reports/**` | Harness, Compatibility, and baseline evidence | Preserve as factual reports; Q01 may reference them but does not edit them. |
| `packaging/**` | Deferred release and artifact reference input | Preserve as packaging control-plane history; later generated-artifact work may reference it. |
| `environments/**` | Compatibility and Harness evidence input | Preserve environment control-plane records; do not claim reproducible bring-up is complete. |
| `.agents/**` | Control support and operational skills | Preserve repo-local skills; Q01 does not change them. |
| `.aide/**` | Control source of truth for queue and policy | Update only Q01 queue status, evidence, and index entries. |
| `docs/constitution/**` | Durable doctrine and invariants | Add Q01 index and reboot doctrine. |
| `docs/charters/**` | Architecture charters | Add Core, Contract, Harness, Compatibility, Hosts, Bridges, Control, and SDK charters. |
| `docs/roadmap/**` | Queue and staged expansion plans | Add queue and staged expansion roadmaps. |
| `docs/design-mining/**` | Candidate lesson extraction home | Add minimal index and candidate list only. |
| `docs/decisions/**` | ADR-like reboot decisions | Add initial decisions required by Q01. |
| `docs/reference/**` | Operational references | Add migration, terminology, command, and generated-artifact references. |

## No-Move Rule

Q01 does not delete, hide, relocate, or rewrite bootstrap-era records. Later queue items may propose moves only with explicit scope, evidence, migration plan, and review approval.
