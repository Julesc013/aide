# AIDE Queue Roadmap

## Purpose

This roadmap summarizes the canonical filesystem queue for reboot work. The source of truth remains `.aide/queue/index.yaml`; this document is a human-readable guide.

## Current Sequence

| Queue Item | Intent | Current View |
| --- | --- | --- |
| `Q00-bootstrap-audit` | Freeze bootstrap-era facts and define the in-place reboot baseline. | needs review |
| `Q01-documentation-split` | Split documentation into durable families and document canonical architecture. | needs review |
| `Q02-structural-skeleton` | Add the smallest filesystem skeleton for Contract, Harness, Compatibility, and Dominium Bridge. | needs review |
| `Q03-profile-contract-v0` | Define initial profile and contract records. | needs review |
| `Q04-harness-v0` | Add first deterministic Harness checks. | passed with notes |
| `Q05-generated-artifacts-v0` | Define generated artifact boundaries and drift evidence. | needs review; review evidence records notes |
| `Q06-compatibility-baseline` | Reconcile bootstrap-era compatibility evidence with the reboot model. | needs review; review evidence records notes |
| `Q07-dominium-bridge-baseline` | Define Dominium Bridge and XStack proof boundaries. | passed with notes |
| `Q08-self-hosting-automation` | Improve queue and worker automation after earlier evidence is reviewed. | passed with notes |
| `Q09-token-survival-core` | Add state reconciliation, compact packets, estimates, and evidence-review discipline. | passed with notes by QFIX-01 |
| `Q10-aide-lite-hardening` | Harden no-install AIDE Lite pack, adapt, validate, estimate, snapshot, and selftest behavior. | passed with notes by QFIX-01 |
| `Q11-context-compiler-v0` | Build compact repo-map, test-map, context-index, context packet, and exact-reference generation beyond shallow snapshots. | passed with notes by QFIX-01 |
| `Q12-verifier-v0` | Add mechanical verifier and evidence packet checks on top of compact context. | passed with notes by QFIX-01 |
| `Q13-evidence-review-workflow` | Generate compact review packets from verifier and evidence output. | passed with notes by QFIX-01 |
| `Q14-token-ledger-savings-report` | Record estimated token metadata, compare compact packets to named baselines, and warn on budgets/regressions. | passed with notes by QFIX-01 |
| `Q15-golden-tasks-v0` | Run deterministic local golden tasks over token-saving workflow quality gates. | passed with notes by QFIX-01 |
| `Q16-outcome-controller-v0` | Turn local token, verifier, review, golden-task, context, and adapter outcomes into advisory recommendations. | passed with notes by QFIX-01 |
| `Q17-router-profile-v0` | Define advisory route classes, hard floors, model/provider metadata, and route decisions without provider/model calls. | passed with notes by QFIX-01 |
| `Q18-cache-local-state-boundary` | Define `.aide.local/` local-state protection and deterministic cache-key metadata before Gateway/cache/provider work. | passed with notes by QFIX-01 |
| `Q19-gateway-architecture-skeleton` | Expose local health, status, route explanation, summaries, and version metadata without provider/model calls or proxy forwarding. | passed with notes by QFIX-01 |
| `Q20-provider-adapter-v0` | Define offline provider contracts and capability metadata without credentials, probes, provider/model calls, or Gateway forwarding. | passed with notes by QFIX-01 |
| `QCHECK-token-survival-foundation-audit` | Audit Q09-Q20 for truth, tests, consistency, and token-survival value. | needs review |
| `QFIX-01-foundation-review-reconciliation` | Reconcile Q09-Q20 source-of-truth state after the checkpoint audit. | needs review |
| `QFIX-02-aide-lite-test-discovery-runner` | Establish the canonical AIDE Lite test command and document the hidden-path unittest limitation. | needs review |
| `Q21-cross-repo-pack-export-import-v0` | Export and fixture-import a portable AIDE Lite Pack without copying AIDE source identity, queue history, generated state, local state, or secrets. | needs review |

## Processing Rule

Future agents should process the next pending queue item by reading its task packet, maintaining its ExecPlan as a living document, writing evidence, running validation, and stopping at review gates.
