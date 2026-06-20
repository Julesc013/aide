# Cursor Type Scan

Independent recursive JSON inspection over all MCP fixtures found:

```text
independent_mcp_fixture_check PASS fixtures=15 indexed=15
```

Every present `cursor` and `nextCursor` value is a string. No absent cursor or
nextCursor is represented by `null`.
