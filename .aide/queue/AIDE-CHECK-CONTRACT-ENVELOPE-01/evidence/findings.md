# Findings

## Finding 1

- Severity: warning
- Finding: `.aide/protocol/aide-envelope.schema.json` is not wired into runtime
  validation.
- Evidence: `contract-envelope validate` validates projections through
  `core/protocol/envelope.py::validate_envelope`; the schema parses and matches
  the helper shape but is not invoked by validation.
- Impact: non-blocking for this slice because the helper tests and direct
  negative behavior checks pass; this limits how strongly the schema can be
  treated as executable conformance.
- Recommended action: run `AIDE-BUILD-CONTRACT-ENVELOPE-HARDEN-01` to either
  wire schema validation into the command or explicitly mark the schema
  reference-only until a conformance runner exists.

No blocking defects were found.
