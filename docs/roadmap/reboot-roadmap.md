# AIDE Reboot Roadmap

## Scope

This roadmap defines the queue-driven reboot path from Q00 through Q08. It is not a release schedule and does not override existing governance, support policy, capability levels, or recorded evidence.

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

## First Shipped Stack

The first shipped stack is Contract + Harness + Compatibility + Dominium Bridge. Q00 records this as direction; it does not implement the stack.

## Later Candidate Tracks

These tracks are deferred until the Q00 through Q08 sequence produces evidence and review approval:

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
