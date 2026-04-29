# AIDE Queue Roadmap

## Purpose

This roadmap summarizes the canonical filesystem queue for reboot work. The source of truth remains `.aide/queue/index.yaml`; this document is a human-readable guide.

## Current Sequence

| Queue Item | Intent | Q01 View |
| --- | --- | --- |
| `Q00-bootstrap-audit` | Freeze bootstrap-era facts and define the in-place reboot baseline. | needs review |
| `Q01-documentation-split` | Split documentation into durable families and document canonical architecture. | needs review after Q01 implementation |
| `Q02-structural-skeleton` | Add the smallest filesystem skeleton for Contract, Harness, Compatibility, and Dominium Bridge. | planned |
| `Q03-profile-contract-v0` | Define initial profile and contract records. | planned |
| `Q04-harness-v0` | Add first deterministic Harness checks. | planned |
| `Q05-generated-artifacts-v0` | Define generated artifact boundaries and drift evidence. | planned |
| `Q06-compatibility-baseline` | Reconcile bootstrap-era compatibility evidence with the reboot model. | planned |
| `Q07-dominium-bridge-baseline` | Define Dominium Bridge and XStack proof boundaries. | planned |
| `Q08-self-hosting-automation` | Improve queue and worker automation after earlier evidence is reviewed. | planned |

## Processing Rule

Future agents should process the next pending queue item by reading its task packet, maintaining its ExecPlan as a living document, writing evidence, running validation, and stopping at review gates.
