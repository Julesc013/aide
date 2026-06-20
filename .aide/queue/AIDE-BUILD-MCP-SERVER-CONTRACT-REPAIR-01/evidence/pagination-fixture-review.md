# Pagination Fixture Review

Before repair, six list fixtures emitted `cursor: null` or
`nextCursor: null`.

After repair:

- `resources-list-request.json` omits `params` when no cursor exists.
- `tools-list-request.json` omits `params` when no cursor exists.
- `prompts-list-request.json` omits `params` when no cursor exists.
- `resources-list-result.json` omits `nextCursor` when no next page exists.
- `tools-list-result.json` omits `nextCursor` when no next page exists.
- `prompts-list-result.json` omits `nextCursor` when no next page exists.

The validator rejects explicit null cursor fields and non-string present cursor
values.
