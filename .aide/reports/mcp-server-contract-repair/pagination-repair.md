# Pagination Repair

The generated no-cursor list request fixtures now omit `params`:

- `resources-list-request.json`
- `tools-list-request.json`
- `prompts-list-request.json`

The generated no-next-page list result fixtures now omit `nextCursor`:

- `resources-list-result.json`
- `tools-list-result.json`
- `prompts-list-result.json`

`validate_fixtures()` now fails explicit `cursor: null`, explicit
`nextCursor: null`, and non-string present cursor values for projected
paginated list families.
