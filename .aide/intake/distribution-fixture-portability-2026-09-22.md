# Bounded source candidate: distribution fixture portability

Candidate task: AIDE-BUILD-DISTRIBUTION-FIXTURE-PORTABILITY-01
Parent programme: AIDE-CONVERGENCE-AND-DELIVERY-01
Admission: proposed for canonical queue; no queue reroute or acceptance performed.
Baseline: dev d37219026462d5670f7a724980faf07e30abb85f.

## Intent and scope

The owner requests actual implementation and testing toward the next stable AIDE
release. This candidate fixes reproducible defects in existing fixture-only
path/snapshot/restore helpers and retains reusable regression tests. It does not
pretend to implement the full specification draft.

Allowed source paths:
- core/distribution/temp_workspace.py
- core/distribution/operation_executor.py
- .aide/scripts/tests/test_aide_distribution_fixture_portability.py
- docs/reference/distribution-fixture-portability.md
- this intake record

## Work performed

1. Captured and Git-blob-verified the baseline modules.
2. Reproduced nine failing cases on disposable files.
3. Centralized portable path checks; retained legacy diagnostic codes.
4. Hardened fixture preflight, snapshot handling, rollback input validation and
   add-file non-overwrite behavior.
5. Executed 125 focused tests, AST parsing, branch coverage and patch hygiene.

Baseline blobs:
- temp_workspace.py: 6b734f9a13fe75866a7ec071cf4cc41d56675ed1
- operation_executor.py: cbf118cb9388fb050526084d65310edadb70302a
- __init__.py: 7caa925ded166a3f812243353ec2cca2e6fdbb23

## Evidence boundary

Observed: nine baseline failures; 125 passing focused tests, no errors or skips;
95% workspace-helper / 81% operation-executor branch-aware coverage. Linux and
CPython 3.13.5 only. No external model sessions or paid API calls were made.
Not run: full repository validation, existing end-to-end distribution suite,
Windows/macOS native profiles, independent review, stable-release qualification.
The container could not clone GitHub; source was reconstructed from exact
connector-read Git blobs. This is not a full-checkout test claim.

## Integration gate

Review and materialize a bounded child WorkUnit under the live canonical queue,
including normal PLANS.md/IMPLEMENT.md and queue-index registration. Recheck the
base and affected blobs; run the complete distribution suite, full AIDE validation
and native profiles. Preserve the existing broker/isolation continuation. Do not
merge this candidate or label it accepted until those gates pass.

No root-authority changes, configuration pins, credentials, downstream mutation,
main/dev promotion, tag, release or operational activation is included.
