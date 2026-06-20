# Independent Probes

Independent JSON probes were run without importing the MCP production helper:

- parsed every MCP JSON fixture;
- searched all fixture trees for `cursor` and `nextCursor` values that were
  not strings;
- confirmed generated no-cursor list requests omit `cursor`;
- confirmed generated no-next-page list results omit `nextCursor`;
- confirmed `resource-not-found-refusal.json` uses `-32002`;
- confirmed the custom refusal codes `-32040`, `-32041`, and `-32042` remain
  present for their existing AIDE-specific refusal fixtures.

The final probe output is recorded in `validation.md`.
