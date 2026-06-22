# Extension Authority Review

The check injected authority-changing extension keys into bundle, metadata,
record metadata, record spec, and nested extension locations, then invoked
production validation in subprocesses.

- denied cases: `80`
- denied cases passed: `80`
- benign cases: `20`
- benign cases passed: `20`
- required error code: `extension.authority_change`

Denied cases included case, camelCase, snake, kebab, dot, slash, and Unicode
compatibility variants. Benign keys such as `vendor.color`,
`documentation.note`, `ui.group`, and `source.annotation` did not trigger the
authority-change error.
