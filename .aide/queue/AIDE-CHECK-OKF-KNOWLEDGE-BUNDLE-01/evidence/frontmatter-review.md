# Frontmatter Review

Result: `PASS_WITH_WARNINGS`.

The generated concept pages use deterministic frontmatter with AIDE-oriented fields such as:

- `type`
- `title`
- `resource`
- `aide_uri`
- `aide_kind`
- `schema_ref`
- `aide_status`
- `generated_from`
- `source_refs`
- `evidence_refs`
- `report_refs`
- `event_refs`
- `source_hashes`
- `explicit_non_capabilities`

`okf validate` reports:

- all concepts have frontmatter: `true`
- all concepts have non-empty `type`: `true`
- AIDE refs parse: `true`
- event refs parse: `true`

Warning:

- Full YAML parser integration is not present. The helper uses a deterministic stdlib structural frontmatter subset.

This warning is non-blocking for the bounded build because the task explicitly allowed deterministic structural validation and did not require a full YAML dependency.
