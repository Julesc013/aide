# Review repair validation

Source changes supersede candidate 5ea1f7cdd53c79a98843a09686ef7bfc7fe9c88e,
tree fb769c0d029c2b4cbbb7db49922515c64e79dd2f. The independent verdict remains
REQUEST_CHANGES, preserved as review-5ea1f7cd.md; external original SHA-256
9ece3667590fb5fb79ee2a604042b40e430123db350dd871fd7051931d7ff773.

Repairs: lexical presence before recovery/retirement; actual Windows Job
membership and source/CLI binding before source commands; packaging refusal
while its canonical output reservation is unqualified; portable compatibility
and explicit exclusion of the source-only resource test from Lite exports.

Command (Windows, Python 3.14; explicit existing fixture parent):

    AIDE_RESOURCE_TEST_PARENT=D:\Projects\AIDE\_recovery\resource-cleanup-20260926
    py -3 -B -m unittest discover -s .aide/scripts/tests -p test_managed_workspace.py -v

Result: 17 tests passed, no skips, 22.209 seconds, exit 0. Tiny fixtures retired.
Includes real broken junction recovery refusal, real Job context, environment
spoof refusal, source entrypoint refusal, portable compatibility, disk/memory
admission, concurrent reservation refusal, bounded logs, cancellation/crash
recovery, monitor failure, inspection and collection retirement.

Four changed Python modules compiled and git diff --check passed. Final
independent acceptance and affected host replay are required. Full importer,
artifact projection, integration and release acceptance have not passed here.

Cleanup receipts are separate from test evidence. Thirty-three physical
checkouts were removed without force or branch deletion; the third-round
receipt is worktree-retirement-third.json. capacity-after-third.json is an OS
snapshot, not a claim that all observed disk recovery came from AIDE cleanup.
