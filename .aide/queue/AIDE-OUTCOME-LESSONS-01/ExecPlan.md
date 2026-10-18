# Correctable, source-linked lessons

## Objective and observed gap
Baseline 3dad27442fcf13e70cd02e633c6a38380b1e4959. The outcome owner preserves opaque metadata and notes, but
has no scoped lesson selection, source-digest freshness or retirement behavior.
Concrete consumer: the next author of portable validation fixtures should discover
the retained lesson from AIDE-VALIDATION-OUTPUT-01's two real fixture failures
before repeating them. This is a bounded P6/P10 contribution, not learned quality,
semantic truth, approval verification or automatic optimization.

## Contract and existing owners
Add read-only outcome lessons --path FILE [--json] using the existing ledger.
Keep ledger writes, current-run replacement, recommendation rules and all existing
tests unchanged. A small pure outcome_lessons helper owns data validation/selection;
the CLI owns bounded repository reads using existing path/secret-like exclusions.
Deliver the helper through the existing portable-helper allowlist.

Optional lesson metadata has schema aide.outcome-lesson.v1, stable id,
positive revision, state active/retired, concise summary, exact repository-relative
applies_to paths, evidence path/SHA256 pairs, supersedes (null at1, canonical
SHA256 of previous lesson thereafter), required_features
revision_chain/source_sha256/advisory_only. Optional unfamiliar fields remain
opaque and participate in identity; unfamiliar schema/required semantics refuse.
All revisions1..latest must be unique, contiguous and predecessor-bound.
Corrections/retirement are newly attributed ledger rows with distinct run identity;
original rows remain. Selection never resurrects an earlier active revision when
the latest is retired, stale or invalid. Structural validity is not authorship.

Limit ledger1MiB/2048 rows,256 lesson revisions,16 exact applicability paths and
8 evidence references per revision,128 distinct evidence references/32MiB aggregate across two reads,
128KiB each. Require canonical safe relative paths and exact lowercase SHA256.
Use finite, duplicate-safe JSON and existing outcome known-field validation.
Read evidence only for latest active matching lessons. Display reasons for excluded
lessons without selecting their text; selected text remains advisory data.
Ledger missing differs from no applicable lesson; malformed/ambiguous/unsafe ledger
refuses without a partial success or writes. Evidence missing/stale/unreadable
excludes that lesson. Re-read ledger and selected evidence before returning to
detect observed changes; this is a local snapshot, not filesystem isolation.

## Scope and sequence
1. Independent admission; guarded local task/aide-outcome-lessons-01 from baseline.
2. Implement helper, CLI, tests and reference/policy. Append exactly one reviewed
   source-local lesson from the completed validation task; byte-preserve original
   ledger prefix. Do not export source-local lesson history to adopting projects.
3. Source job: new lesson tests plus all20 unchanged outcome-controller methods.
   Cover correction/retirement, stale/missing/out-of-scope selection, ambiguous or
   unfamiliar required metadata, bounded unsafe reads, real separate CLI processes
   and no writes. Actual source lesson lookup must identify the known failure and
   exact unchanged source/evidence; no fabricated history.
4. Separately reviewed capability binding refresh/owned export. Delivered tests
   plus actual safe-installed consumer (record, inspect, correct, retire through
   project-owned ledger revisions), preserving customization and helper identity.
5. Fixed changelog preview, terminal review and fresh dev/main synchronization;
   retire only this closed local task. Preserve qualification branch and release.

At most3 separately reviewed managed jobs: source, export/delivered/installed,
preview. Existing180sec/1GiB/32MiB scratch/8MiB retained/4GiB reserves unchanged.
No additional model/API call, endpoint, source checkout, provider or release effect.
Use unchanged qualified evidence selectively; preserve all failures and stop on
drift/unresolved review/failed admission instead of retrying or relaxing assertions.

## Verification and recovery
Tests must show an older active lesson is not returned after correction/retirement
and source changes exclude its advice. Unknown optional metadata survives unchanged.
Real consumers execute actual exported/installed bytes without source fallback.
Preserve old ledger and scope all append effects. Preview is not publication.
Exact integration receipts govern refs. Existing desktop binding, DiskEd ownership,
Lite successor owner decisions and whole-outcome measurements remain separate.

## Progress
Read-only investigation and bounded candidate prepared; no implementation or job.

Admission ACCEPT. Guarded local branch and source preparation complete; no jobs yet.

Source36 and actual source lesson PASS, job5a9a5b8d retired/collected. Existing binding refresh CURRENT; classification unchanged. Delivered and installed tests prepared, not yet run.

Consumer job2 PASS: delivered36/ownership6/exporter checks, actual safe-installed correction/retirement/stale evidence/customization and no-write inventories. Both jobs retired/collected. Fixed preview remains separately gated; published assets unchanged.
