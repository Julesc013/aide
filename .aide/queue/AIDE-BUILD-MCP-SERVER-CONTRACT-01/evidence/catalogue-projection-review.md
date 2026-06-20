# Catalogue Projection Review

Generated static catalogues:

- `.aide/interop/mcp/resource-catalog.json`: 10 resource projections
- `.aide/interop/mcp/tool-catalog.json`: 7 future read-only/report-only tools
- `.aide/interop/mcp/prompt-catalog.json`: empty prompt catalogue
- `.aide/interop/mcp/capability-catalog.json`: contract/runtime capability matrix

Every tool records:

- `side_effect_class: read_only_or_report_only`
- `execution_status: not_implemented`
- `callable: false`

No mutation-capable tool such as `aide.patch.apply`, `aide.work.run`,
`aide.worker.dispatch`, `aide.branch.create`, or `aide.release.publish` is
declared.

Resource catalogues are generated projections. AIDE queue, protocol, evidence,
and OKF records remain authoritative.
