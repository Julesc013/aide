# Malformed Commit Report

Status: complete for review.

Generated report: `.aide/changelog/malformed-commits.md`

Current preview range `HEAD latest 50 commits` reports 13 malformed or legacy commits. The findings are older pre-Q27/Q34-style commits with missing structured Markdown headings and missing machine-readable changelog categories.

Examples include:

- `776ada192ed4 test: cover adapter compiler behavior`
- `e2088aed6dd3 docs: document existing tool adapter compiler`
- `05330b0842a3 fix: harden q25 pack provenance validation`

These do not block preview generation. Future release promotion should review them and decide whether warnings are acceptable; Q34 does not rewrite history.
