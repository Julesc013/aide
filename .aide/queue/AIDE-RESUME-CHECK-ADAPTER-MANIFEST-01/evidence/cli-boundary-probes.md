# CLI Boundary Probes

Required commands return `PASS_WITH_WARNINGS`:

- `adapter-manifest status`
- `adapter-manifest project`
- `adapter-manifest validate`

Unsupported operations fail closed:

- `adapter-manifest apply`
- `adapter-manifest approve`
- `adapter-manifest execute`
- `adapter-manifest rollback`
