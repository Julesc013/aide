# Extracted consumers and first committed-source replay

The frozen source is `e215698a993d1904152c614ec84b71741f4bb086`.
The first artifact projection commit is
`d4311651b76d5a6c2896dd897b7751f416924baf`, tree
`b622194aae2e4e70a81506b2433fec5a6751950f`.

Independent reviewer `/root/safe_import_implementation` returned ACCEPT for
the **local artifact and disposable-consumer scope only**. The external original
`D:\Projects\AIDE\_review_scratch\repair-staging-e215698a-consumer-20260925\qualification-verdict.json`
has SHA-256 `c07f7406cf01549cf5f0640e150589838bd9f7fd99e9f24c0dcc1491d587107e`.
Its final evidence JSON SHA-256 is
`f4d4470881934c32b8a32e0b9f2bf929bf61e96376cd834d5ce6c1ea85c63fe5`;
delivered-stage race JSON SHA-256 is
`442b5fba8c692b36cd3e28b37b6fa9d1edbb793f02c74adef2036b3a1e561383`.
The reviewer checked 833 equal safe regular ZIP/tar members, 830 portable pack
checksums, seven release checksums, and source-export provenance. A fresh ZIP
and brownfield tar consumer passed 16 offline commands covering import,
installed doctor, exact owned repair, direct-edit preservation and read-only
removal planning. Eight delivered-script race cases for repair intent/payload
staging writer denial and competing-target no-clobber passed. Brownfield
authored AGENTS prefix, unknown file, and project state were retained.
ZIP SHA-256 `949cfc24ac261f2db520e8c1c4e80f46d9f9ac569ae6c6d5ea62c6e0c31434ec`;
tar.gz SHA-256 `26081af25c94d8494542b120ce1adee4df27710e089f65f707daecf8db679c2f`.
Both archive hashes matched the committed Git blobs and remained unchanged
after consumers.

From clean `d4311651`, `release bundle`, `release validate`, `release draft`,
and `release draft-validate` each exited zero. The first replay changed 18 of
44 tracked release files as pack provenance changed from current-source PASS
to valid `PASS_SOURCE_ANCESTOR`; the ZIP and tar hashes stayed identical.
The before path/hash list is
`D:\Projects\AIDE\_review_scratch\repair-staging-projection-release-hashes.txt`
(SHA-256 `ea624ef374938b30c41e048f50d55bafd0ed681437cd4070d57c9895ce856299`);
the after list is
`D:\Projects\AIDE\_review_scratch\repair-staging-replay1-release-hashes.txt`
(SHA-256 `7d80dacc3bf5b3351cf67b0208c797c218f5cd9e42688ef734b496a632427ccd`).
This transition is an expected metadata convergence, not a changed archive.
Commit the converged metadata and repeat all four commands from clean HEAD;
zero changed release files is still required before dev integration.

This local acceptance does not qualify safe import writes, complete lifecycle,
native/hosted effects, main promotion, or public stable release.
