# Commit Discipline

Q27 defines AIDE's changelog-ready commit standard. New AIDE-managed queue work
uses:

```text
type(scope): summary
```

Subjects must be specific, 72 characters or fewer, and must not end with a
period. Substantive commits require these Markdown body sections:

- `## Summary`
- `## Why`
- `## Changed`
- `## Validation`
- `## Changelog`
- `## Risks`
- `## Follow-up`

Run:

```powershell
py -3 .aide/scripts/aide_lite.py commit check --latest
py -3 .aide/scripts/aide_lite.py commit check --range HEAD~5..HEAD
py -3 .aide/scripts/aide_lite.py commit template
```

The optional hook is installed only when explicitly requested:

```powershell
py -3 .aide/scripts/aide_lite.py commit install-hook
```

Q27 does not rewrite old commits. Malformed history is reported and future
release/changelog tooling consumes the structured body categories and AIDE
trailers.
