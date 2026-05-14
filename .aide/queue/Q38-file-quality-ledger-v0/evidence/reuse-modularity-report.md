# Q38 Reuse And Modularity Report

## Generated Reports

- Module report: `.aide/reports/module-quality-report.md`
- Reuse report: `.aide/reports/reuse-modularity-report.md`
- Commands:
  - `py -3 .aide/scripts/aide_lite.py quality modules`
  - `py -3 .aide/scripts/aide_lite.py quality reuse`

## Findings

- Large module candidates: 1
- Mixed-purpose candidates: 1
- Reuse candidates: 274
- Duplicate content and similar filename groups are candidate-only signals.

## Interpretation

Q38 identifies review candidates where deterministic evidence suggests a file
may be large, mixed-purpose, duplicated, or related to repeated helper names.
It does not propose extraction, movement, deletion, or path changes.

## Caveats

- Similar filenames and repeated helper names can reflect valid generated
  templates, tests, policy variants, or export-pack content.
- Q38 does not compute semantic duplication.
- Refactor decisions belong to Q39 and later review-gated phases.
