# Report Consistency Review

MCP build reports and artifacts parse as JSON where applicable.

Observed counts agree across contract and build reports:

- resources: `10`
- tools: `7`
- prompts: `0`
- fixtures: `15`
- transports: `2`
- conformance expectations: `22`

The reports agree that no tool is callable, no resource is served, no endpoint
is live, and no runtime behavior exists.

The reports do not detect the two material standards-alignment defects recorded
by this independent check.
