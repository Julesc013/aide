# Path Scope Acceptance

Accepted:

- drive-prefixed paths fail closed;
- duplicate-normalized paths fail closed in `allowed_paths`, `forbidden_paths`,
  and `declared_changed_paths`;
- diagnostics preserve original values and canonical collision path;
- absolute path, traversal, forbidden match, outside-allowed, overlap, empty,
  dot-only, and prefix-boundary protections remain intact.

No broad path-policy engine or case-folding policy is accepted.
