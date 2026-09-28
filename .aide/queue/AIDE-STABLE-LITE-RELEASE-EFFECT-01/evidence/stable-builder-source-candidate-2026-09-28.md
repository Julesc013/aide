# Distinct first-stable source candidate — 2026-09-28

Base local and remote `dev` was `f3f59303e5d09683a6345be8cbada06496ec4ff9`,
tree `90789f4081332bc407284c17e8193392c365db3c`. This candidate changes
only the AIDE Lite release command, Q47 regression test, release policy/docs,
and this task's queue/evidence records. Resolve its exact commit/tree from Git
after committing; the source review must name them and must not cover later
generated asset bytes automatically.

The task allowlist adds `DOCUMENTATION.md` for the required root index update
after the release policy/reference changed. This is an owner-delegated narrow
scope correction, not a new product surface.

The `release stable-build` path is distinct from Q47/Q48 preview generation.
It requires a clean-provenance pack, existing validated first-stable policy,
exact source commit/tree and shared managed runner admission; it creates
versioned archives under `.aide/release/stable/` with embedded version/profile
identity and checksummed marker, plus a separate asset manifest/SHA256SUMS.
The first-stable builder permits `1.0.0` and no published predecessors only;
the final history check and version selection remain effect obligations.
`stable-validate` checks assets, pack and policy binding, archive shape,
embedded identity, and checksums. Archive validation refuses escaping,
duplicate, nonregular and oversized members before fixture extraction. It
does not create a Git tag, GitHub Release or public support claim.

Adversarial source checklist: invalid version, stale/dirty pack, existing tag,
unapproved source changes, redirected/unknown output, post-build asset tamper,
and interrupted exact-output replay are refused or safely reconciled by the
new path. The test directly covers distinct preview/stable bytes, clean replay,
tamper detection and exact-output recovery; a tiny ZIP traversal and tar link
fixture proves extraction is not attempted for unsafe input. Scope remains a
single local first-stable release mechanism, not a general release scheduler.

Final code SHA-256 `.aide/scripts/aide_lite.py`:
`95f9b17b454989dd9891b69893efa431b9434b385a4c282660edce22918a27e6`.
Final Q47 test SHA-256:
`a33838dc8a3f31a722d1e0fc166ba473e07a2de4736ed5d472e705768df3d4f0`.
Policy digest `release-versioning.yaml` is bound in the managed job manifest
and will be embedded in final candidate assets.

The final D-managed Q47/Q48 job `c1267714e2bc4d5289959e94cd61b619`
ran 33 tests in 62.246 seconds, all passed. It peaked at 3,103,945 scratch
bytes and 276,402,176 process-memory bytes; scratch retired and reservation
released. Exact manifest SHA-256
`0214a7c609bcf50127bc8349010b52c6e6efe1d8a80d0c2686ce6373aadb93f0`
and receipt SHA-256
`1a163702a2e6acbe1b20229ff1f1b15c9fbd763224d812fdccebb1514af8f543`.
The earlier final-code focused job `d4d32756aee44b1e9bc81b30020c97a2`
passed one test in 8.574 seconds, retired scratch and reservation.
The installed release commands and final generated asset consumers remain
unrun. Independent source review is required before dev integration and
generation of final release candidate bytes.
