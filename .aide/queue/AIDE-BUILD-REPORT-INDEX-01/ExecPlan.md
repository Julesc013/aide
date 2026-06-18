# ExecPlan: AIDE-BUILD-REPORT-INDEX-01

## Purpose

Build a deterministic index over existing tracked `.aide/reports` files so
AIDE can discover report subjects, stages, producers, evidence refs, related
reports, and ambiguity without restructuring report storage.

## Scope

Allowed writes are limited to this queue packet, the report index projection,
self-management report-index reports, and focused implementation/tests.

The task does not move, rename, rewrite, repair, normalize, delete, or migrate
historic reports. It does not rewrite evidence refs.

## Current Facts

- `AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01` is built but not independently
  checked or accepted.
- The report index may consume that build output only as provisional,
  unaccepted information.
- Existing report directories and filenames retain historic conventions.

## Milestones

1. Implement report index module.
2. Add focused tests.
3. Generate index and report projections.
4. Validate deterministic rerun and self-output exclusion.
5. Stop at `needs_review`.

## Validation Plan

- Focused unit tests.
- Python compile.
- Deterministic rerun hash comparison.
- JSON/YAML parse.
- Markdown/JSON finding agreement.
- Task inspect/evidence.
- Broad doctor and validate.
- Commit policy check after commit.

## Progress

- [x] Module implemented.
- [x] Focused tests added.
- [x] Index and reports generated.
- [x] Focused tests, compile, validator, and deterministic rerun passed.
- [x] Task evidence written.
- [ ] Commit and post-commit validation.

## Recovery

If resumed, rerun `py -3 -m core.reconciler.report_index`, then
`validate_report_index_reports('.')`, focused tests, task inspect, and task
evidence. Do not proceed if report files were modified outside the allowed
index outputs.

## Retrospective

The index preserves old report paths and records ambiguity instead of
normalizing historic layout.
