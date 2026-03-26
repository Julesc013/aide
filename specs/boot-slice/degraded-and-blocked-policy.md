# Degraded And Blocked Policy

## Purpose

The first boot slice must progress without pretending that all lanes can reach the same proof depth at the same time.

## Acceptable Degraded Proofs

The following degraded proofs are acceptable in the first wave when they are documented explicitly:

- report-only proof: `boot.slice.invoke` succeeds and returns deterministic report output, but `boot.slice.editor-marker` remains deferred
- preview-only proof: the lane computes and presents the deterministic marker edit without applying it automatically
- companion-only first proof: a family reaches the boot slice first through its companion lane while the deeper native lane remains blocked
- archival-native proof: a retired or historical native lane proves entry point plus report behavior and records archival evidence, even if richer editor wiring is deferred

## Unacceptable Shortcuts

The following do not count as valid degraded proofs:

- silent omission of capability reporting
- silent omission of unavailable reasons
- skipping the oldest lane in a family without a recorded blocker
- claiming a deeper editor or workspace proof than the evidence supports

## Blocked-Lane Handling

A lane is blocked when it cannot honestly satisfy its minimum accepted proof because of a concrete blocker such as:

- no reproducible environment
- no viable entry-point surface
- unresolved host contract ambiguity that prevents implementation choice
- missing packaging or runtime prerequisites needed for the first invocation

Blocked lanes must be recorded explicitly. They must not be rewritten as if they merely were not attempted.

## Stop Conditions

Implementation work for a lane should stop and record a blocker when:

- the minimum accepted proof cannot be defined without inventing host behavior
- the required environment or tooling is unavailable
- the entry-point surface cannot be invoked meaningfully in the current phase

Once the blocker is recorded, the program may continue with:

- the family fallback lane if one exists
- the next unblocked lane in the same rollout phase

## Promotion Criteria

A degraded proof can be promoted later when:

- the existing report-first proof is stable
- capability reporting remains consistent with matrices and manifests
- a previously deferred editor proof becomes implementable
- the required environment or packaging blocker is resolved

Promotion does not erase the degraded record. It supersedes it with a richer proof.
