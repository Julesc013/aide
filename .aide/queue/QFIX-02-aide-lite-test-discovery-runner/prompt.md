# QFIX-02 Prompt Summary

Implement a bounded AIDE Lite validation-surface repair after QFIX-01.

Required outcomes:

- Diagnose why `py -3 -m unittest discover -s .aide/scripts/tests -t .`
  fails.
- Establish one canonical AIDE Lite test command.
- Preserve direct `selftest`.
- Add or update tests so the canonical command and importability do not regress.
- Update command catalog and compact docs.
- Write QFIX-02 evidence and stop at `needs_review`.

Explicitly forbidden:

- Q21 export/import or cross-repo pilots.
- Gateway forwarding, provider calls, model calls, runtime/UI work, autonomous
  loops, secrets, raw prompt logs, raw response logs, or `.aide.local/` state.
