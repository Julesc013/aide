# Canonical output reservations

Existing generator outputs stay at .aide/export/aide-lite-pack-v0 and
.aide/release. Evaluation keeps .aide/evals/runs. A job may declare only these
existing ordinary roots, their actual volume identity and positive byte budgets;
the combined budgets must fit a finite local canonical_bytes allowance.
Admission counts these reservations together with scratch and collection peaks.
OS monitoring covers every declared volume; metadata scans are bounded to the
declared trees, every thirty seconds and at completion. Canonical outputs are
retained in place; overrun fails qualification without deleting them.

The generator's accepted algorithms, portable behavior and artifact identity
rules remain unchanged. This adds source entrypoint reservation requirements,
not a scheduler, a filesystem quota or permanent machine placement.

Validation, Windows/Python 3.14, explicit existing tiny-fixture parent:

    py -3 -B -m unittest discover -s .aide/scripts/tests -p test_managed_workspace.py -v

PASS: 22 tests, no skips, 21.894 seconds, exit 0. Five added cases cover finite
reservations, non-fallback root refusal, separate volume sampling, a real
junction, real fast output overrun with canonical bytes preserved, and source
command manifest requirements. Tiny fixtures retired; no bulk allocation.

Independent source acceptance for prior candidate 11226a6e is preserved in
review-11226a6e.md, external original SHA-256
625cd4bdde5915a57c5b5ea9c567e9a47c99374e22e5e07cf68cd56ebc4ea8dc.
It does not accept this changed source or final artifacts. An actual host replay
at 11226a6e passed ten cases in 3.335s; bounded-host-check.json binds exact
inputs/manifest and bounded-host-check.txt retains its 1,434-byte log once.
Observed peak Job memory 59,314,176 bytes, scratch absent, reservation released.

Next: exact technical delta review, approved local permanent pool configuration,
then actual importer/generator qualification under admission. Packaging and
stable release acceptance are not claimed by synthetic fixtures.
