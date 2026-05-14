# Q38 Docs Consistency Report

## Generated Report

- Report path: `.aide/reports/docs-consistency-report.md`
- Source map: `.aide/repo/doc-link-map.json`
- Command: `py -3 .aide/scripts/aide_lite.py quality docs`

## Findings

- Stale doc reference candidates: 718
- Missing doc candidates: 63
- Public surface missing doc candidates: 63

## Interpretation

These are conservative warnings. A stale reference candidate means the
deterministic path scanner found a path-like reference that does not currently
resolve as a repo path. It is not proof that the documentation is wrong without
review.

Missing doc candidates prioritize active source/tool/policy/contract-like
surfaces that lack obvious documentation references from Q37 doc-link data.

## Caveats

- Inline examples, historical references, generated export-pack payload refs,
  and policy examples can produce false positives.
- Q38 does not rewrite documentation or repair links. Future WorkUnits should
  inspect specific candidates before editing.
