# Control Charter

## Purpose

Control owns AIDE's operating boundaries: queue policy, autonomy levels, review gates, bypass rules, execution records, and evidence expectations.

## Owned Responsibilities

- Keep `.aide/queue/` canonical for non-trivial work.
- Require ExecPlans for long-running autonomous tasks.
- Enforce review gates for permission widening, destructive actions, generated artifact source-of-truth changes, compatibility changes, releases, merge-to-main actions, and policy changes.
- Keep generated outputs deterministic and reviewable when later queue items introduce them.

## Non-goals

- Control is not a full autonomous runner.
- Control does not bypass human review.
- Q01 does not implement Q08 self-hosting automation.

## Boundaries

- Small direct work may use the bypass policy only when it is trivial or low risk.
- Queue tasks must stop at blockers and review gates.
- Control policy changes themselves are review-gated.

## Relation To AIDE Core / Hosts / Bridges

Control is an internal AIDE Core domain. It governs Core, Hosts, and Bridges work without becoming a product runtime or host adapter.

## Current Status

Current status: partial. The filesystem queue, policies, and helper scripts exist. Autonomous worker invocation remains deferred.
