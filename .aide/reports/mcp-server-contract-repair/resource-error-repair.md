# Resource Error Repair

`resource-not-found-refusal.json` now uses:

```json
{
  "code": -32002,
  "message": "Resource not found"
}
```

The bounded AIDE metadata in `error.data` remains present. Unrelated custom
AIDE refusal codes remain distinct:

- `tools-call-refusal.json`: `-32040`
- `protocol-version-refusal.json`: `-32041`
- `capability-refusal.json`: `-32042`
