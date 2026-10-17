# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 33a377743d86f59fd63a042096063d664e200468..1a342812969951b09f06595c8cda98b6b9082081
source_head: 1a342812969951b09f06595c8cda98b6b9082081
preview_only: true

## Highlights

- Added: quality explain-file --json with explicit unverified freshness and heuristic coverage. (5fa78ca78afb)
- Added: exported quality explain-file --json with bounded output and explicit evidence limits. (1a3428129699)
- Changed: quality discovery source evidence and portable qualification preparation. (35a3a9035abc)

## Validation Summary

- 5fa78ca78afb: PASS: doctor, full validation and diff checks; NOT RUN: exact managed fixture run follows independent effect review.
- 35a3a9035abc: PASS: 23 source methods, zero skips/errors/failures; collection, quiescence and retirement verified. NOT RUN: second export allocation.
- 1a3428129699: PASS: 23 source methods,16 exported Q38 methods,six ownership checks,export/doctor/validate/pack-status and unchanged published assets. NOT RUN: preview allocation3.

## Known Risks

- 5fa78ca78afb: Source revision is attribution only; similarity does not prove semantic equivalence or safe extraction.
- 35a3a9035abc: Unknown freshness and heuristic coverage remain explicit. Source acceptance is not release or native-host qualification.
- 1a3428129699: No semantic completeness,current-byte freshness,live host delivery or new release qualification is implied.

## Follow-up

- 5fa78ca78afb: Run admitted checks, qualify changed export, independently review and synchronize dev/main; public1.0.0 unchanged.
- 35a3a9035abc: Execute independently accepted allocation2, review generated outputs, preview and integrate qualified dev/main.
- 1a3428129699: Run the independently reviewed preview,then exact terminal integration and remote verification.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
