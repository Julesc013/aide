# Cursor Probes

Temporary in-memory validator probes passed.

Valid cases:

- `cursor: "opaque-cursor-value"` passes.
- `nextCursor: "opaque-next-cursor"` passes.

Invalid cases fail for `resources/list`, `tools/list`, and `prompts/list`:

- null
- number
- boolean
- object
- array

Cursor strings remain opaque; the validator does not parse semantics, numeric
ordering, encoding, or cursor content.
