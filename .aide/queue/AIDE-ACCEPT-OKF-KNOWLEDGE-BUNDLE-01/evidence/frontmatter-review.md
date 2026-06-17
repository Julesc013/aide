# Frontmatter Review

Result: `ACCEPTED_WITH_WARNINGS`.

Accepted frontmatter rules:

- concept documents have deterministic frontmatter
- concept documents have a non-empty `type`
- unknown fields and unknown types are tolerated unless they violate AIDE reference, event reference, source/evidence traceability, or authority-boundary rules
- `index.md` and `log.md` are reserved files and do not require concept frontmatter
- the field name for non-capabilities is `explicit_non_capabilities`

Validation observations:

- `all_concepts_have_frontmatter: true`
- `all_concepts_have_non_empty_type: true`
- `aide_refs_parse: true`
- `event_refs_parse: true`

Warning disposition:

- Full YAML parser integration remains deferred.
- The stdlib structural frontmatter subset is accepted for this bounded projection slice only.
