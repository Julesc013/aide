# CRLF managed-section review repair

## Frozen rejected subject and independent finding

The independent reviewer `/root/owned_repair_integration_review` returned
`REQUEST_CHANGES` for source commit
`acbcb9c8bd628d714a2457adc54e90563ce23126`, tree
`19d743c8ee94e30cb9da0ec00fc995183574eead`. The external original is
`D:/Projects/AIDE/_review_scratch/three-way-acbcb9c8-independent-source-review.md`,
SHA-256 `44b16319b404e8efde5456cdf7946ecc3269b3453d5fd5a34d7c9c0476ae2c24`.
Its exact disposable reproduction log has SHA-256
`4e31914d420c425674723ddc0bd7aa3e74d43fc7cbfeff5b322343980c8d3280`.
The candidate falsely conflicted when a receipt-owned `AGENTS.md` block was
rendered with authored CRLF and upstream changed: installed and source block
digests correctly differed, while ownership remained `aide_portable_managed`
and `local_overlay: false`.

The broad importer command started on that rejected source was interrupted
after this finding. Its external log is zero bytes (SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`),
and its exit was 1. It has no test-result status and is not reused.

## Repair and executed regression

The new Windows regression freezes checksum-valid upstream pack changes and
tests both v1 and v2 receipts, exact authored CRLF bytes outside the managed
block, a later unrelated update, a direct managed-block edit, recorded overlay
preservation, and changed-upstream conflict refusal. On rejected source
`acbcb9c8`, both receipt-version subtests failed at the expected
`conflict` versus `update_owned` assertion. The external red log is
`D:/Projects/AIDE/_review_scratch/three-way-crlf-red-acbcb9c8.log`, exit 1,
SHA-256 `70842c7f2e2c2080a8b12482cc5c57e354b842debf4dc482bda5dc49f2202c4e`.

The repair keys receipt-owned eligibility to the observed installed block
digest plus validated `aide_portable_managed` ownership and no local overlay.
When upstream is unchanged and that installed block still matches, it keeps
the section `unchanged` instead of misclassifying rendered CRLF as a new
project overlay. A true project edit remains `preserve_local` on unchanged
upstream and conflicts on changed upstream. The extended regression passed
1/1 with both subtests in 71.588 seconds, exit 0, external log
`D:/Projects/AIDE/_review_scratch/three-way-crlf-green-extended.log`, SHA-256
`5de83e617495cd2ab3f3515fd06070fb3f2b96cb8ce8ee28674fb1d1d417a1f4`.

Exact repaired source SHA-256:
`0e18e752c61ab11aa994a6afac42490ad7419ffb44f8af6f4f3d409972780cd3`.
Exact tests SHA-256:
`eea08577f9f814f081e866938b06046930791f704d0d85b99c8dd60f3bf62e2f`.
The full importer suite started on those hashes and is still pending when
this record was written. Its external log is
`D:/Projects/AIDE/_review_scratch/three-way-full-importer-crlf-repair.log`;
no exit or pass is claimed yet. Independent delta review, artifact generation,
consumer checks, replay and dev integration remain open.
