# Failed Check Preservation

The original failed check remains preserved:

- `.aide/reports/mcp-server-contract-check/check-report.json`:
  `sha256:d25088895080eec7806e771c4861679a50868cf3223f98da556ed6d98e4ce6c8`
- `.aide/reports/mcp-server-contract-check/findings.md`:
  `sha256:e32a0b575d8638884a4c06e46d660531d7c6675fa91df063cb228381b6d4c2f1`

The failed check still records exactly two material findings:

1. optional `cursor` / `nextCursor` fields emitted as JSON `null`;
2. MCP resource-not-found using `-32043` rather than `-32002`.
