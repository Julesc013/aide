# Non-Capability Review

ProjectLock v0 remains a proposed selection and binding object only.

Explicit false capability flags were independently checked:

- `install_apply_implemented: false`
- `update_apply_implemented: false`
- `target_repository_mutation_implemented: false`
- `admission_implemented: false`
- `authorization_implemented: false`

The `project-lock` CLI exposes only:

- `status`
- `project`
- `validate`

The unsupported command `project-lock apply` exits with code `2` through
argparse invalid-choice handling and no apply implementation is exposed.

Disposition: `CLOSED`.
