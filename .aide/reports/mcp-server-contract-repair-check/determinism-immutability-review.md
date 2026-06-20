# Determinism And Immutability Review

Repeated projection remained deterministic:

- `mcp-server-contract project`: `PASS_WITH_WARNINGS`
- `mcp-server-contract validate`: `PASS_WITH_WARNINGS`
- `deterministic_projection: true`
- `source_artifacts_mutated: false`

After projection and validation, the worktree remained clean before the
repair-check packet was written.

Predecessor hash snapshots remained unchanged:

- `.aide/interop/exports/manifest.json`:
  `sha256:747b0e83042f7184748b0f58ae2d90ee69a6b944c8d67900819cdd419c9a2bfd`
- `.aide/interop/exports/mcp-manifest.preview.json`:
  `sha256:5f2d61b339dabb617533dd8caa72d6ca1c2b26d279c4b3bb38e05bea972f8cc8`
- `.aide/reports/mcp-server-contract-check/check-report.json`:
  `sha256:d25088895080eec7806e771c4861679a50868cf3223f98da556ed6d98e4ce6c8`
- `.aide/reports/mcp-server-contract-check/findings.md`:
  `sha256:e32a0b575d8638884a4c06e46d660531d7c6675fa91df063cb228381b6d4c2f1`
- `.aide/reports/mcp-server-contract-repair/repair-report.json`:
  `sha256:c83497b7bd8c957b9b4e42324e753550f6650bd72d083016aec655742f579f88`
