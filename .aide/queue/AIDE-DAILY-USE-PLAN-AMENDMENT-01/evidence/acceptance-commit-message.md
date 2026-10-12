chore(task): record independent daily-use planning acceptance

## Summary

- Record the actual independent ACCEPT_WITH_NOTES for AIDE-DAILY-USE-PLAN-AMENDMENT-01.
- Bind acceptance to exact source922173c8/tree7c701ed1 and retain operational gates.

## Why

- The owner authorized separate campaign reviewers and the source review completed.
- Queue state must reflect the actual verdict and route the next ready work.

## Changed

- Preserve the reviewer identity, exact subject, checks and nonblocking dispositions.
- Close planning acceptance and route the existing campaign back to SESSION.

## Validation

- PASS: independent full-range scope, fourteen added links and retained receipt hashes.
- PASS: plan structure and six negative cases; prior doctor/validate exits zero.
- PASS: metadata diff and generated-manifest checks at closeout.
- NOT RUN: source integration and operational effects require separate exact review.

## Changelog

- Internal: accepted workflow planning is now linked to an actual independent verdict.
- Follow-up: qualify the actual host through existing SESSION mechanisms.

## Risks

- All three review notes are nonblocking for this source subject and explicitly disposed.
- Runtime/target/source-integration claims remain outside this verdict.

## Follow-up

- Prepare and review exact new-host resource setup and one supported-route qualification.

AIDE-Task: AIDE-DAILY-USE-PLAN-AMENDMENT-01
AIDE-Phase: independent-planning-acceptance
AIDE-Result: PASS_WITH_NOTES
AIDE-Scope: task and parent acceptance records, queue index and generated manifest
AIDE-Token-Impact: prior valid checks reused; review usage unknown
AIDE-Quality-Gate: exact independent acceptance; operational gates retained
