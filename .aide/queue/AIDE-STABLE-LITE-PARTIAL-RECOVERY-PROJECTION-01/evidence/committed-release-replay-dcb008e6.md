# Committed release replay, 2026-09-28

Second six-command replay from clean `dcb008e62b46f4f11d1c2b01a7c04833b72c92e7`
exited zero in every D managed job, with scratch retired and reservations
released, but changed 30 generated paths. The exact external JSONL result is
`D:\Projects\AIDE\.aide.local\execution\control\projection-replay-dcb008e6-results.jsonl`,
SHA-256 `517507ab736a349ace123fcc73ccbb1d89d5f69e42a30c5d262eb74deae2b72b`.
This is a retained **failed zero-change** result. The export manifest advanced
its `source_commit` from `4b5854f2` to `dcb008e6`; the generator always uses
current HEAD, so including it in a clean postcommit replay causes another
change after any commit. The 30 derivative changes were restored only after
the receipt was retained. No source or task changes were restored.

The established committed projection gate consists of `release bundle`,
`release validate`, `release draft`, and `release draft-validate`, with separate
`pack-status` provenance and boundary validation. From clean `dcb008e6`, all
four D managed jobs exited zero, retired scratch and released reservations.
Their external result is
`D:\Projects\AIDE\.aide.local\execution\control\release-replay1-dcb008e6-results.jsonl`,
SHA-256 `50d8ab741f8269e81754f4f161dac5525753f0ea7ebc985f3187fd61d0cc1397`.
`pack-status` returned `PASS_SOURCE_ANCESTOR`, valid checksums and boundary,
zero problems. This first four-command replay **failed zero-change** with
exactly 18 `.aide/release/**` metadata paths changed. Committed ZIP
SHA-256 `af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`
and tar SHA-256 `f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725`
remained unchanged. A final replay from a clean convergence commit is required.
