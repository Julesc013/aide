# Validation

Review238fa7bc REQUEST_CHANGES for one stale derived helper binding. Explicit
capability ledger refresh now identifies the unchanged tested helper
ba7f4957/2,379,708 bytes. Final doctor/validate reran against those bytes and
retain only the two known export-provenance failures plus doctor's aggregate
failure. Original structural observation/review remain preserved; source PASS74
is reused for identical production/tests/execution inputs. New exact review pending.

Admission: actual independent ACCEPT for proposal101f243f, with no notes.
Baseline source tests:10 run with8 original failures,0 errors/skips; expected
defects reproduced against unchanged source7fbf8e11. Full output preserved.
Final source/compatibility tests:74 PASS,0 failures/errors/skips against exact
fc8a68b7/tree880f44fa; six named modules. Both managed jobs retired and every
collected digest matches; no active attempt remains. See verification.json.
Changed-path verifier and Harness validation PASS. Source AST and actual named
packet preparation PASS; packet uses1,281 estimated tokens (chars/4).
Doctor and validate FAIL with two current-source export provenance failures;
full original logs/digests remain in source-structural-observation.json. No
expected result was changed and no archive was rebuilt. Required package refresh
and replay remain separately scoped. Exact source and integration review pending.
