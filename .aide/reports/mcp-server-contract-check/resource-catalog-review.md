# Resource Catalog Review

Resource catalogue count: `10`

All resource URIs are unique, bounded `aide://` projections, and do not expose
arbitrary filesystem paths, `file://` paths, `.aide.local`, credentials, or raw
environment values.

Every resource remains `not_served_contract_only`.

Material finding `MCP-CHECK-001` affects `resources/list` pagination shape, not
the resource URI inventory itself.
