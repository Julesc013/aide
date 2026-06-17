# Frontmatter Review

The helper writes deterministic YAML-style frontmatter using a conservative stdlib-parseable subset. No new YAML dependency was added.

Implemented functions include:

- `write_frontmatter`
- `parse_frontmatter`
- `validate_frontmatter`
- `build_concept_page`
- `write_concept_page`

The validator checks:

- non-reserved concept pages have frontmatter
- non-reserved concept pages have non-empty `type`
- `explicit_non_capabilities` is used instead of `not_capabilities` or `non_capabilities`
- `aide://` refs parse through the accepted ReferenceID helper where present
- `event_refs` use `aide://event/...`

Warning disposition: `full YAML parser unavailable; stdlib structural frontmatter validation used` is non-blocking for this slice.
