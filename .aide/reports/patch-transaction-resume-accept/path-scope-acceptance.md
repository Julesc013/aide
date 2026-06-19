# Path Scope Acceptance

Accepted path-scope behavior:

- Windows drive-prefixed paths fail closed.
- Duplicate-normalized paths fail closed in `allowed_paths`,
  `forbidden_paths`, and `declared_changed_paths`.
- Absolute paths, traversal, empty paths, dot-only paths, declared paths outside
  allowed scope, forbidden matches, direct overlap, and prefix-boundary mistakes
  fail closed.
- Diagnostics for duplicate-normalized paths preserve both original inputs and
  the shared canonical value.

Not accepted:

- broad path-policy engine;
- case-folding collision policy;
- target-repository apply safety.
