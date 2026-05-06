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
| `Q09-token-survival-core` | Add state reconciliation, compact packets, estimates, and evidence-review discipline. | needs review |
| `Q10-aide-lite-hardening` | Harden no-install AIDE Lite pack, adapt, validate, estimate, snapshot, and selftest behavior. | needs review |
| `Q11-context-compiler-v0` | Build compact repo-map and context-reference generation beyond shallow snapshots. | recommended next; not implemented |

## Processing Rule

Future agents should process the next pending queue item by reading its task packet, maintaining its ExecPlan as a living document, writing evidence, running validation, and stopping at review gates.
