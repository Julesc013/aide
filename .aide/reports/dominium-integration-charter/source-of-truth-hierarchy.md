# Source-Of-Truth Hierarchy

## AIDE

| Tier | Authority | Consumers | Mutation Owner | Projection Rules | Conflict Resolution |
| --- | --- | --- | --- | --- | --- |
| Profile and policy | `.aide/profile.yaml`, `.aide/policies/**`, `.aide/queue/policy.yaml` | queue, reports, future adapters | AIDE queue tasks | project only with provenance | policy wins over reports |
| Queue | `.aide/queue/index.yaml`, task `status.yaml`, task packets | agents, reports, final answers | queue task owner | generated packets are advisory | queue truth wins over chat |
| Accepted protocol evidence | accepted task status/reports/evidence | future seams and charters | accepted queue tasks | cite by task and digest | accepted evidence wins over roadmap |
| Reports/OKF/RepoGraph | `.aide/reports/**`, `.aide/knowledge/**`, `.aide/repo/**` | humans and tools | report tasks | evidence/projection only | never canonical by convenience |
| Runtime-local/chat | local state, chat, memory | orientation only | none | may not authorize work | lowest authority |

## Dominium

| Tier | Authority | Consumers | Mutation Owner | Projection Rules | Conflict Resolution |
| --- | --- | --- | --- | --- | --- |
| Canon/glossary | `docs/canon/constitution_v1.md`, `docs/canon/glossary_v1.md` | all Dominium surfaces | Dominium governance | may be summarized with refs | canon wins |
| Agent governance | `AGENTS.md` | agents/tools | Dominium governance | generated mirrors derive from it | AGENTS wins over generated mirrors |
| Scope contracts | command/service/module/refusal/diagnostic/capability/project graph contracts | bridge, Workbench, validators | Dominium contract tasks | versioned refs only | contract wins for public surface |
| Current queue | `.aide/queue/current.toml` | task planning | Dominium queue tasks | snapshot only | live queue wins over stale plans |
| Evidence/audits | `docs/repo/audits/**` and validation outputs | AIDE charter and future checks | Dominium tasks | evidence only | preserve provenance |
| Generated/archive/chat | mirrors, archives, chat | orientation | none | non-canonical | lowest authority |

Cross-repo conflicts stop the integration path until a bounded check or reconciliation task resolves the conflict. AIDE does not flatten Dominium authority order into AIDE queue order.

Generated reports are not canonical. Generated projections are not canonical unless a later reviewed policy explicitly marks them canonical.
