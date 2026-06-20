# Determinism And Immutability Review

`mcp-server-contract project` and `mcp-server-contract validate` report
`PASS_WITH_WARNINGS`, deterministic projection remains true, and source
artifact mutation remains false.

Accepted Interop Export artifacts retained their pre-repair hashes:

- `.aide/interop/exports/manifest.json`
- `.aide/interop/exports/mcp-manifest.preview.json`

The failed-check report hashes were preserved for:

- `.aide/reports/mcp-server-contract-check/check-report.json`
- `.aide/reports/mcp-server-contract-check/findings.md`

Repeated projection byte comparison passed with 45 files compared.
