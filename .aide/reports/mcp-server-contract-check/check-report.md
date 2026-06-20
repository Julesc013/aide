# MCP Server Contract Check Report

## Result

`FAILED_VALIDATION`

## Source Chain

- `AIDE-ACCEPT-INTEROP-EXPORTS-01`: `ACCEPTED_WITH_WARNINGS`
- `AIDE-BUILD-MCP-SERVER-CONTRACT-01`: `PASS_WITH_WARNINGS`
- Checked commit: `c8a143f76af585ae3a0cc3004fb5278c57f264e0`
- Build evidence: `missing_evidence: 0`

## Material Findings

1. `MCP-CHECK-001`: list request/result fixtures emit `null` for optional
   `cursor` and `nextCursor` fields. Under the pinned subset checked here,
   those fields must be omitted when absent or be strings when present.
2. `MCP-CHECK-002`: `resource-not-found-refusal.json` uses error code
   `-32043`. The prompt's pinned MCP resource-not-found mapping is `-32002`.

## Passing Areas

- JSON files parse.
- Envelope shape, contract identity, protocol version pin, and JSON-RPC version
  are present.
- Initialization fixtures preserve initialize, initialize result, and
  initialized notification order.
- Client and server capabilities are separated.
- Resource URIs are bounded `aide://` projections.
- Tools are read-only or report-only and `callable: false`.
- Prompt catalogue is empty and structurally consistent.
- Runtime facts remain false.
- Unsupported CLI operations fail closed.
- Repeated projection is byte-stable in the current Python 3.14 shell path.

## Recommendation

Do not accept MCP server contract. Queue:

`AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`
