# Skill Catalogue Review

Generated projection:

- `.aide/interop/a2a/skill-catalog.json`

The contract declares four future read-only discovery skill candidates:

- `aide.queue.inspect`
- `aide.evidence.inspect`
- `aide.capability.inspect`
- `aide.context.inspect`

Each skill is marked:

- `implemented: false`
- `requires_future_policy_decision: true`
- `requires_future_capability_grant: true`
- `side_effect_class: read_only_or_report_only`

Focused tests verify stable skill IDs, duplicate rejection, forbidden mutating
segments, and implemented-skill overclaims.
