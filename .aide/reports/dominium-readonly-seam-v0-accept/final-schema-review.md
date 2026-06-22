# Final Schema Review

The final Repair 05 check independently traversed the public schema and recorded:

- object_count: `55`
- unclassified_object_count: `0`
- unintentionally_open_object_count: `0`
- extension_ref_count: `10`

The accepted schema surface is meaningfully constrained for the read-only seam
scope. External Draft 2020-12 validation remains warning debt because
`jsonschema` is not installed in this environment.
