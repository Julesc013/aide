# Post-projection release metadata convergence

Projection commit `d0bfa4045a3cf9c58abdc77b72a2ab50273ab32b`, tree
`64df0bd0e0123f630f8fce7430de636a037567ef`, contains the exact
consumer-tested ZIP SHA-256
`8c4fbef71470954c64dbd09e181384a3fbff0ec997a799ef197f0f6cce1e07f6`
and tar.gz SHA-256
`11c95b9c10355cb617225472cd0c72cbf8a9bbe62671d6926bd28512967aa34c`.
Both remain bound to clean source `8365aa61`.

The first post-commit replay ran `release bundle`, `release validate`,
`release draft` and `release draft-validate` from clean `d0bfa404`; all four
exited 0. External receipt:
`D:/Projects/AIDE/_review_scratch/stable-contract-projection-d0bfa404-replay1-commands.txt`.
Log SHA-256 values, in that order:

1. `d26ec14f98a8a359121a2db16a1208d012406c5f4ecef2bcf08e1aa58a6e6fe8`
2. `c30eb7108e7489ec43f1f401bf9c07f08a111c52ddac098830e65daf5910e770`
3. `d8c9c7b0dd2a75cb3514f6a4f8d282c03b8f286da9db9ba61781fc31c8ba117d`
4. `13103d0bfd1ae6bd60f6e12e9c4d0a9337f3e68b7f599f35c72d82634b8545de`

The replay **did not pass the zero-change gate**: exactly 18 tracked
`.aide/release/**` metadata files changed as the committed pack was classified
with `PASS_SOURCE_ANCESTOR` and corresponding source/validation fields were
refreshed. Neither archive changed. This is a bounded metadata convergence,
not a new source or archive build. Commit these 18 current outputs coherently,
then rerun the four release commands from that exact commit and require zero
tracked changes. Until that check passes, no dev effect is qualified.
