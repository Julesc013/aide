# ExecPlan: AIDE-BUILD-GENERATED-OUTPUT-LEDGER-01

## Purpose

Build a deterministic generated-output ledger that classifies tracked generated,
projected, exported, report, OKF, context, and tool-specific interop artifacts.

## Scope

Allowed writes are limited to the queue packet, generated-output ledger,
self-management reports, and the focused implementation/tests.

The task is classification-only. It does not regenerate, delete, repair, move,
rename, normalize, rewrite references, migrate reports, or apply changes.

## Current Facts

- `AIDE-ACCEPT-DOC-KNOWLEDGE-TRUTH-RECONCILER-01` is accepted with warnings.
- Generated downstream artifacts are non-canonical unless reviewed policy says
  otherwise.
- `.aide/generated/manifest.yaml` records the Q05 generated target set.
- Root authority policy classifies `.aide/reports`, `.aide/generated`,
  `.aide/repo`, `.aide/roots`, `.aide/refactors`, `.aide/tools`, and related
  outputs as generated evidence/previews/indexes/advisory reports by default.

## Milestones

1. Implement deterministic classification module.
2. Add focused tests.
3. Generate ledger and reports.
4. Validate deterministic rerun and no source mutation.
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
- [x] Ledger and reports generated.
- [x] Focused tests, compile, validator, and deterministic rerun passed.
- [x] Task evidence written.
- [ ] Commit and post-commit validation.

## Recovery

If resumed, rerun `py -3 -m core.reconciler.generated_output_ledger`, then
`validate_generated_output_ledger_reports('.')`, focused tests, task inspect,
and task evidence. Do not proceed if output becomes nondeterministic or if any
source/projection file is repaired.

## Retrospective

The ledger deliberately preserves unknown generator, freshness, source, and
consumer classifications instead of guessing.
