# Q37 File Classification Report

## Classification Rules

The classifier uses deterministic path, extension, and marker rules from
`.aide/policies/file-classification.yaml` and `.aide/policies/repo-intelligence.yaml`.

- Source-like extensions under non-test/doc/policy paths classify as `source`
  or `tool` depending on path.
- `tests/`, `test/`, `core/*/tests`, and `.aide/scripts/tests` classify as
  `test`.
- Markdown and docs paths classify as `doc`, except queue/evidence/report paths
  which classify as `evidence`.
- `.aide/policies/**` classify as `policy`.
- `.schema.json` and contract paths classify as `schema` or `contract`.
- `.aide/export/**`, `.aide/context/latest-*`, `.aide/intake/latest-*`, and
  other latest/generated paths classify as generated/evidence when applicable.
- Template paths and managed-section markers are flagged as templates or
  generated outputs.

## Counts

- kind counts: contract 10, doc 313, evidence 500, fixture 109, generated 324,
  policy 43, schema 9, source 37, template 11, test 35, tool 6, unknown 146.
- status counts: active 562, evidence_only 500, generated 324,
  template_only 11, unknown 146.

## Unknown Examples

- `.aide.local.example/config.example.yaml`
- `.aide/adapters/catalog.yaml`
- `.aide/adapters/targets.yaml`
- `.aide/cache/key-policy.yaml`
- `.aide/cache/latest-cache-keys.json`
- `.aide/changelog/config.yaml`
- `.aide/commands/catalog.yaml`
- `.aide/compat/deprecations.yaml`

## Boundary Notes

Unknown does not mean unused or low quality. Q37 does not score files or
recommend deletion. Unknown files are inputs for Q38 File Quality Ledger and
later refactor-control review.
