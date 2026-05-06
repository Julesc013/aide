# AIDE Reboot Roadmap

## Scope

This roadmap defines the queue-driven reboot path that started at Q00 and now extends through the token-survival sequence. It is not a release schedule and does not override existing governance, support policy, capability levels, or recorded evidence.

## Queue Sequence

| Queue Item | Title | Intent | Status At Q00 |
| --- | --- | --- | --- |
| `Q00-bootstrap-audit` | Baseline freeze and reboot audit | Freeze current repository facts, preserve bootstrap-era history, and define the reboot baseline. | implemented by this task and awaiting review |
| `Q01-documentation-split` | Documentation split and canonical architecture | Split reboot docs into canonical architecture and reference surfaces for AIDE Core, AIDE Hosts, and AIDE Bridges. | planned |
| `Q02-structural-skeleton` | Structural skeleton | Add only the minimal filesystem skeleton justified by Q00 and Q01. | planned |
| `Q03-profile-contract-v0` | Profile contract v0 | Define initial profile and contract records for self-hosting work. | planned |
| `Q04-harness-v0` | Harness v0 | Add first deterministic harness checks for the reboot profile. | planned |
| `Q05-generated-artifacts-v0` | Generated artifacts v0 | Define deterministic generated-output boundaries and drift evidence. | planned |
| `Q06-compatibility-baseline` | Compatibility baseline | Reconcile bootstrap inventory, matrices, and compatibility posture with the reboot model. | planned |
| `Q07-dominium-bridge-baseline` | Dominium Bridge baseline | Define Dominium Bridge and XStack proof boundaries without broad runtime work. | planned |
| `Q08-self-hosting-automation` | Self-hosting automation | Improve queue and worker automation after the prior queue evidence is reviewed. | planned |
| `Q09-token-survival-core` | State reconciliation and token survival core | Reconcile post-Q08 state and add compact packets, estimates, evidence review, and no-history guidance. | implemented and awaiting review |
| `Q10-aide-lite-hardening` | AIDE Lite hardening | Make the Q09 no-install helper deterministic, drift-aware, budget-aware, and self-tested. | implemented and awaiting review |
| `Q11-context-compiler-v0` | Context Compiler v0 | Build repo-map, test-map, context-index, context packet, and exact context-reference generation beyond shallow snapshots. | implemented and awaiting review |
| `Q12-verifier-v0` | Verifier v0 | Add mechanical checks for evidence packets, file refs, generated drift, forbidden paths, and diff scope. | implemented and awaiting review |
| `Q13-evidence-review-workflow` | Evidence Review Workflow | Generate compact review packets from task packet, evidence packet, verifier result, changed files, validation, and risks. | implemented and awaiting review |
| `Q14-token-ledger-savings-report` | Token Ledger and Savings Report | Record estimated token metadata, named baselines, budget status, regression warnings, and compact savings summaries. | implemented and awaiting review |

For the Q01 documentation view of this sequence, see [Queue Roadmap](queue-roadmap.md). For later deferred tracks, see [Staged Expansion Roadmap](staged-expansion-roadmap.md).

## First Shipped Stack

The first shipped stack is Contract + Harness + Compatibility + Dominium Bridge. Q00 records this as direction; it does not implement the stack.

## Later Candidate Tracks

These tracks are deferred until the queue sequence produces evidence and review approval:

- pack, skill, and workflow IR
- GStack and reference imports
- Runtime
- CLI or Service surfaces
- Commander
- Mobile
- IDE Hosts
- release and packaging automation

## Roadmap Discipline

- Keep queue items small enough to review.
- Stop at review gates.
- Treat generated outputs as deterministic and reviewable.
- Preserve bootstrap-era evidence.
- Do not promote candidate tracks into committed implementation without queue evidence.
