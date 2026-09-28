# Current-source importer qualification and bounded evidence reuse — 2026-09-28

Current task source `c6de695fbbd8c120802c4334c70cca9cd9f0cf1a`, tree
`1f4ae8a6dc58b4bfd221d145598082cf7607201d`, ran the A–M importer
partition in D job `ee68c416cc2a4b8fa848934f8f355fc6`. Its manifest
SHA-256 was `c83ed9414ea0936c35bd9dfe00614e4c370814441c3b0ef29c00577f411baf0d`.
**54 tests passed**, no skips, in 2,608.382 seconds. Child exit zero; peak
scratch 20,658,738 bytes, peak memory 248,217,600 bytes; scratch retired and
reservation released. Retained receipt SHA-256
`0f01c711152541393837a53ab9e50bae84ea29769891060cbb3a9053cf38bdb2`.

The prior O–Z D partition at source
`8040b10a5d2c894e4f78b234d6fb55ed9403d391` remains retained as job
`673c9cc6696a42739d9734679c0868ad`, receipt SHA-256
`44895fc4fe59a7206562695746e2a4c66ab021a96f6934a4f7ebc17459185c79`:
**56 tests passed**, no skips, in 3,218.922 seconds, exit zero with scratch
retired and reservation released. This is **reused prior evidence**, not a
current-source rerun. The importer implementation
`.aide/scripts/aide_lite.py` has identical SHA-256
`25829e62e404a78c8fd053d3917909381cb9d31785a1df6af86370895e87451c`;
the importer oracle `.aide/scripts/tests/test_export_import.py` has identical
SHA-256 `46f5fce38c32c60a96e8b473417b8034072710218266be1aab6820fd90587d84`.
The Python executable and shared D configuration digests are also unchanged.
Of the 11 altered input hashes in the O–Z manifests, three are generated
export metadata, six are queue/plan/evidence records, and the remaining two
are the managed runner and its tests. The runner's changed retirement path
is covered by the current A–M job and 27 focused tests, including a real Git
readonly scratch canary. Per-job environment digests differ because job IDs
and temp paths differ; they are not represented as byte-identical.

This pair covers all 110 importer methods once under the same importer code
and oracle; the O–Z partition is explicitly reused under the binding above.
Source qualification does not establish all candidate public forms from final
published bytes, native child network tracing, a frozen release manifest,
independent release ACCEPT, main promotion or publication.
