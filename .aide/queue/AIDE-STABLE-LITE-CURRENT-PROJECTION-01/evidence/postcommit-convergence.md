# Post-projection metadata convergence, 2026-09-25

The projection commit is `dc8697e336eba99b4b855dfec775238e0bb1be17`,
tree `cfc41507015806364a75c2a2cc75d6bd9adcd01e`. It contains the exact
consumer-tested ZIP SHA-256
`68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c`
and tar.gz SHA-256
`d0b424563ea7a85d207546b0e2b0d381641e046659846876adbddf96a954073b`.
Both archives remain bound to clean source `0509e161`.

From clean `dc8697e3`, the first four-command replay ran `release bundle`,
`release validate`, `release draft` and `release draft-validate` serially;
all exited 0. External command/exit/log receipt:
`D:/Projects/AIDE/_review_scratch/stable-lite-current-projection-20260925/postcommit-replay1-receipt.txt`,
SHA-256 `8769852086fb607147128a538dea7d5eb66df898402e21de8253a8af2662e2a7`.

The replay **failed the zero-change gate**: exactly 18 tracked
`.aide/release/**` metadata files changed as the committed pack was classified
`PASS_SOURCE_ANCESTOR`; release validation and asset fields followed that
classification. Neither ZIP nor tar changed. The first replay did not modify
source code, export pack, changelog or artifact bytes.

Commit these 18 current metadata files with this failure record. Then rerun
the same four commands from that clean exact commit and require zero tracked
and untracked changes with unchanged ZIP/tar hashes. Until that succeeds, no
artifact/dev effect is qualified.

## Second replay, passed

Metadata convergence commit `10fd7a207f1644c5966e688092e03387e5e553e8`,
tree `a0888730d121ae88736ba5063f1b15b464e87f69`, retains the exact ZIP/tar
hashes above. From clean `10fd7a20`, the same four release commands all exited
0, changed **zero tracked or untracked files**, and preserved both archive
hashes. External `postcommit-replay2-receipt.txt` SHA-256
`1c06b93fa3958d0221f114f5baf5c4d4e468ffbefab9677658465f4b554e2766`.
The failed first replay remains part of the record. Canonical committed checks
and commit-range policy also passed; see `committed-qualification.md`.
