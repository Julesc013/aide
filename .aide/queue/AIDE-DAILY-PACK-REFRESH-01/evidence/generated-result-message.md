chore(packaging): retain the current source export result

## Summary

- Freeze the regenerated derived pack and actual structural qualification evidence.

## Why

- Accepted task-binding source needs honest current-export correspondence before replay.

## Changed

- Update only known generated pack members/checksums/provenance and add files/.aide/scripts/tests/test_task_binding.py.
- Retain corrected effect acceptance, all six fixture outcomes and complete command/receipt hashes.
- Preserve original startup failure and immutable published asset hashes.

## Validation

- PASS: six fixtures, export, doctor, validate and pack-status with no skipped checks.
- PASS: full output digests, current855-file content, unchanged four assets and job retirement.
- NOT RUN: separately reviewed clean-subject replay remains the final authorised attempt.

## Changelog

- Changed: derived Lite export now corresponds to accepted current source.
- Added: exact regenerated result and retained structural evidence.

## Risks

- Generated-result review must precede this commit; replay and consumers remain separate.

## Follow-up

- Review exact staged tree, commit matched result, then prepare separate clean replay.

AIDE-Task: AIDE-DAILY-PACK-REFRESH-01
AIDE-Phase: exact-generated-outcome
AIDE-Result: needs_review
AIDE-Scope: known derived export, exact evidence and queue/root coherence
AIDE-Token-Impact: zero model requests; source PASS74 reused
AIDE-Quality-Gate: six fixtures/full structural PASS; generated review and replay pending
