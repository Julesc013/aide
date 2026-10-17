# Validation

Current result: source 61, delivered 60, ownership 6 and fixed three-commit
preview PASS. Capability binding CURRENT, classification unchanged. All three
jobs retired; the original allocation 2 wrapper failure remains evidence.
Integration is separately gated and has not executed at this checkpoint.

## Historical preparation and attempt observations

PASS: syntax and all17 original test method ASTs retained.
NOT RUN: reviewed source61, delivered60, ownership6 and fixed-range preview jobs.
Source CLI change invalidates capability binding until its reviewed refresh.

Source61 PASS, zero failures/errors/skips, exact source6a50010b. Old-source
comparison PASS. Jobb93da708 retired, collected hashes verified, scratch absent,
reservation released. Reviewed capability refresh CURRENT; classification unchanged.

Allocation2 FAIL: incorrect expectation for a source-only document; delivered suite
not started. Ownership6/export/doctor/validate/pack-status PASS, exact862members and
two payloads changed. Original receipt/logs preserved; no rerun of successful export.

Final allocation90ca096b PASS: delivered60, zero failures/errors/skips; exact
9a22aa09..cba99132 three-commit preview, six-output replay, zero malformed. Fullpack
and source61 inputs remain exact. All3jobs retired/quiescent, collections verified,
scratch absent and reservations released. No additional allocation is admitted.
