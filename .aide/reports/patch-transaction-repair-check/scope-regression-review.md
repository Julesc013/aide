# Scope Regression Review

Existing scope protections remain intact.

- Direct allowed/forbidden overlap fails.
- Declared paths outside allowed scope fail.
- Declared paths inside forbidden scope fail.
- Prefix boundaries are respected: `src-old/file.py` is not treated as inside
  `src/**`.
- Traversal, absolute paths, empty paths, dot-only paths, and drive-prefixed
  paths fail closed.
- Valid distinct paths remain accepted.

The current implementation treats nested forbidden scope under an allowed scope
as an overlap error. This is existing strict behavior and was not changed by the
repair check.

No case-folding policy is accepted, so case-insensitive collision behavior
remains warning debt rather than a hidden claim.
