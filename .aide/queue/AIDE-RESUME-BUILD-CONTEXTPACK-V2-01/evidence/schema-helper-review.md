# Schema Helper Review

Implemented:

- `.aide/protocol/aide-context-pack-v2.schema.json`
- `core/protocol/context_pack_v2.py`
- `core/protocol/__init__.py` export

The helper projects one deterministic `ContextPack` record with stable identity:

```text
aide://context-pack/minimal-context-pack-v2-01
```

Validation checks required envelope fields, source refs, source hashes, required
sections, capability/conformance/evidence reference kinds, explicit
non-capabilities, and no-execution status facts.
