# Protected Path Checks

Report: `.aide/reports/lifecycle-fixture-rollback-dry-run/protected-path-checks.json`

Result: `PASS`

Protected paths checked:

- `.git`
- `.github`
- `.aide.local`
- `.env`
- `secrets`

Path handling:

- Checked rollback record paths are repo-relative fixture paths.
- Protected target/release/provider/Gateway paths remain blocked.
- Path traversal remains blocked by lifecycle schema validation and fixture checks.

No protected paths were mutated.
