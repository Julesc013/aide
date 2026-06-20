# Resource Error Fixture Review

Before repair:

```json
"code": -32043
```

After repair:

```json
"code": -32002
```

The fixture remains a resource-not-found refusal with bounded AIDE metadata in
`error.data`. Custom AIDE refusal fixtures remain on their prior custom codes.
