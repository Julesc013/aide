# CLI Boundary Review

Checked commands:

- `adapter-manifest status`: `PASS_WITH_WARNINGS`.
- `adapter-manifest project`: `PASS_WITH_WARNINGS`.
- `adapter-manifest validate`: `PASS_WITH_WARNINGS`.

Unsupported commands fail closed through argument validation:

- `adapter-manifest apply`
- `adapter-manifest approve`
- `adapter-manifest execute`
- `adapter-manifest rollback`
