# Post-projection metadata convergence

The frozen local archive projection is commit
`d137f936bf0a161de12c5c478ec7624f04127629`, tree
`232eba32afdecd8f3131c8769923515148b50772`. It contains the reviewed
ZIP SHA-256 `32c1f0ad5465809eec5d8ed64c801e8d3ca31c0fe5840ca41188a376325711f9`
and tar.gz SHA-256
`22101aa98982cf8b88d6a4540d814e9751095207535427a4e5a5fc3f36833044`,
both still bound to clean source `99a9e54d`.

The first post-commit attempt reran `export-pack`, `changelog preview`,
`release bundle` and `release draft`. All four commands exited 0, but the
zero-change check failed: 30 tracked generated files changed. The export and
changelog generators use current HEAD for their own source identities; after
the projection commit, they shifted those identities to `d137f936`. The
failed attempt is retained in external logs named
`combined-update-health-replay-*-d137f936.log` under
`D:/Projects/AIDE/_review_scratch/`. No source file or repository ref changed.
This failed replay is not counted as passing evidence.

I restored only the five changed changelog previews and the export manifest
from frozen commit `d137f936`, preserving the reviewed source/pack binding.
Then `release bundle`, `release validate`, `release draft` and
`release draft-validate` each exited 0. Their log SHA-256 values are:

1. `3ce86b6ae4eb166e2e7d76d68a57e0f77896082461572a17fe17e43884b40090`
2. `c30eb7108e7489ec43f1f401bf9c07f08a111c52ddac098830e65daf5910e770`
3. `88da611652e9735e3077ac53c17af3496a8231375bf530f7922e9ea9537b66bb`
4. `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de`

The resulting 18 tracked diffs are release/draft metadata. They record
`pack_status: PASS_SOURCE_ANCESTOR` and refresh corresponding validation,
install-note and checksum fields. Both reviewed archive hashes are unchanged;
`pack-status` passes with zero problems. A separate coherent metadata commit,
then a second four-command replay with zero changed files, remain required
before the exact `dev` effect review.
