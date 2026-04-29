# Policy Declaration Shape

## Purpose

Policy declarations provide profile-level rules that complement existing queue, autonomy, bypass, and review-gate policies.

## Required Fields

- `schema_version`
- `profile_contract_version`
- `status`
- `principle`
- `rules`

Each rule should include:

- `id`
- `requirement`
- `severity`

## Boundary

Q03 policy files must not loosen existing policies. If a new policy conflicts with a stricter existing policy, the stricter policy wins.
