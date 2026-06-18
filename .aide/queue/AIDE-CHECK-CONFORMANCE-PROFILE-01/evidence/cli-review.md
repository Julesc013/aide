# CLI Review

Result: `PASS`

The CLI exposes only:

- `conformance-profile status`
- `conformance-profile project`
- `conformance-profile validate`

Focused tests confirm forbidden subcommands such as `run`, `execute`, `admit`,
`result`, `adapter-run`, `repair`, and `mutate` are rejected by the parser.
