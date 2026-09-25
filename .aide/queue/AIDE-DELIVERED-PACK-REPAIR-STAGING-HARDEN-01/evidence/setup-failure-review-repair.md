# Superseding setup-failure correction

Independent exact-source review of `1a44ec6175080db6f212f21a133e08e178153596`
found a narrow staging-link leak if descriptor conversion or file-object
setup failed after exclusive stage creation. That source is superseded for
security acceptance. Its focused test result remains historical evidence only.

The correction marks the still-owned stage for deletion through its raw
Windows handle when descriptor conversion fails, or through its CRT-owned
handle when file-object setup fails, before closing that handle. The normal
publication path reuses the same deletion function.

A new Windows regression injects both setup failures and verifies that the
destination remains absent and the staging directory is empty. Command:
`py -3 -B -m unittest discover -s .aide/scripts/tests -p
test_export_import.py -k test_owned_repair_stage_setup_failure_cleans_owned_link`.
Result: PASS, 1 test with two failure subcases. External log:
`D:\Projects\AIDE\_review_scratch\repair-staging-setup-failure-regression.log`,
SHA-256 `b829ac6de712b640abb40e39f8f0acf9fd9980d6fca6a218a5cd347e185c24e2`.
Python compilation and diff whitespace check passed. Full importer and focused
repair reruns, artifact replay, and fresh independent verdict remain pending.

The reviewer also observed that a simulated cleanup failure after a successful
link leaves an exact-byte destination and a residual stage while raising an
exception. Existing intent is retained for recovery. Such an exception is an
uncertain effect and must not be reported as no-effect or blindly replayed.
