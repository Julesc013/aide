# Fixture Corpus Review

The fixture corpus contains:

- Valid fixtures: `8`
- Invalid fixtures: `20`

The production `project-lock validate` command was exercised as the system under
test. Every valid fixture passed and every invalid fixture failed with the
expected refusal subset.

Covered invalid classes include digest mismatch, payload digest mismatch,
missing required component, optional component ambiguity, component digest
mismatch, missing component, unsatisfied dependency, dependency cycle,
unsupported protocol, unknown required feature, required unknown extension,
absolute path, traversal path, secret-like reference, `.aide.local` reference,
source latest reference, source report reference, invalid target overlay, and
unaccepted manifest.

Disposition: `CLOSED`.
