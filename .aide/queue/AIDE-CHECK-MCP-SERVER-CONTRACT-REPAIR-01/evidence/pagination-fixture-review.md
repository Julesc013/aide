# Pagination Fixture Review

Independent fixture parsing verified:

- `resources-list-request.json`: `cursor` absent.
- `tools-list-request.json`: `cursor` absent.
- `prompts-list-request.json`: `cursor` absent.
- `resources-list-result.json`: `nextCursor` absent.
- `tools-list-result.json`: `nextCursor` absent.
- `prompts-list-result.json`: `nextCursor` absent.

No explicit `cursor: null` or `nextCursor: null` remains in the supported
paginated fixture subset.
