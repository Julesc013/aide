# Scope Regression Review

Existing path-scope protections were preserved:

- allowed/forbidden overlap fails;
- declared path outside allowed scope fails;
- declared path inside forbidden scope fails;
- prefix boundary rejects `src-old/file.py` as outside `src/**`;
- traversal and absolute paths fail;
- valid distinct paths remain accepted.

The strict existing behavior that treats nested forbidden scope under an allowed
scope as an overlap error remains unchanged.

No accepted case-folding policy exists.
