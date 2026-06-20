# Validator Hardening

The fixture validator now checks:

- supported paginated request methods have omitted or object `params`;
- present `params.cursor` values are strings;
- supported paginated result fixtures contain their collection and have omitted
  or string `result.nextCursor`;
- `resource-not-found-refusal.json` uses `-32002`;
- custom AIDE refusal fixtures preserve their expected reason codes and custom
  error codes.

The validator remains a bounded helper for this MCP contract slice. It is not a
full official MCP schema validator.
