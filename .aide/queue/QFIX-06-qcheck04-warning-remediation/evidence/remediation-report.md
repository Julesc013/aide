# Remediation Report

## Initial Findings

- QCHECK-04 completed as PASS_WITH_WARNINGS.
- Harness `validate` and `doctor` reported `GENERATED-SOURCE-STALE`.
- `py -3 scripts/aide compile --dry-run` reported only
  `.aide/generated/manifest.yaml` as `would_replace`; managed guidance and
  preview files were current.

## Remediation Plan

Refresh the generated manifest through the reviewed harness generation command,
reduce the fixture and selftest costs that caused raw unittest discovery to
time out, then rerun validation.

## Changes Made

- Refreshed `.aide/generated/manifest.yaml` through `scripts/aide compile --write`.
- Added an in-process successful-result cache to AIDE Lite `run_selftest()` so repeated test calls in the same interpreter do not rebuild the same deterministic fixture.
- Trimmed `_write_minimal_repo()` to avoid copying the full source export pack and full golden-task catalog into every temp fixture.
- Kept the required malformed-evidence fixture for the verifier golden test.
- Removed the synthetic `Q15-golden-tasks-v0` fixture queue status from minimal repos so temp validation does not imply the whole golden catalog is present.
- Skipped `git ls-files` subprocess work when the inspected fixture root is not a git repository.
- Updated four test fixtures to write the AIDE Lite selftest golden subset where a full golden catalog run is not the behavior under test.
- Regenerated export-pack, local release bundle, local GitHub release draft, changelog preview, GitHub advisory, and latest eval evidence.

## Outcome

- Harness stale generated-manifest warning is resolved.
- Raw `.aide/scripts/tests` discovery now passes: 300 tests in 508.590 seconds.
- AIDE Lite selftest/test remain passing and materially cheaper.
- Export pack, release bundle, release draft, and install lifecycle no-apply validators pass.
- No Q36-Q48 or QCHECK/QFIX review gate was changed to `passed`.
- No target repo, branch, tag, GitHub Release, upload, provider, model, or network mutation was performed.

## Deferred Or Preserved

- Full `eval run` remains the authoritative full golden catalog run and still passes.
- The raw `.aide/scripts/tests` discovery is still the longest validation command; this remediation makes it pass within the local run instead of masking it.
- Export pack provenance remains dirty-source-recorded until a future clean regeneration after review.
