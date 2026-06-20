# Secret-Like Scan

The helper validation reports:

- `secret_like_scan_clear: true`

Focused tests check that generated contract data does not contain concrete
secret fragments such as `sk-`, `xoxb-`, `-----BEGIN PRIVATE KEY-----`,
`password=`, or `api_key=`.

Authorization expectation text may mention future token or credential handling
as non-implemented behavior; that wording is not a resolved secret value.
