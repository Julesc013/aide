### Acquisition review and original outcome

Independent ACCEPT covered source 1b321b54, effect 1c2f89bf and template 5fc528ac:
one acquisition-only job, allocation 1 of 4, no downloaded-code execution.
Managed checkpoint c5077b95 and job a6c38b9b343642c6a4d22f74d66e8247 preserve it.

The job FAILED at the explicit 128KiB metadata bound after downloading the Mini
and Pydantic wheels. Mini metadata/notices and all six source/license comparisons
passed. Pydantic's actual METADATA is 133,006 bytes, hash 4d4c8e8d5e6a27d5208f0d7949f25628e6747133034969d4d1399b1ad5394036.
It exceeded 131,072 bytes; this is a measured fixture-bound mismatch. The second
wheel's full archive hash was independently rechecked and matches the original pin.
No imported artifact, installed package or product execution occurred.

The failed job is retired/quiescent with all collection digests verified,
scratch absent and reservation released. Preserve its original raw logs, partial
report and artifacts. Proposed continuation reuses both exact downloaded files,
retains all artifact/source/metadata checks and raises only the per-METADATA
parsing guard to 256KiB. Aggregate expansion and every configured job cap/reserve
remain unchanged. It needs a new exact source/effect review.

Required prechecks passed; retain the separate controller argparse failure from
the mistaken pack status invocation as a non-test outcome. Correct pack-status
returned PASS_SOURCE_ANCESTOR. Full validation retained 60,916 PASS / 1 WARN / 0 FAIL.

**Focused review correction.** The independent reviewer returned REQUEST_CHANGES
for repair map b3d1e4a3: Pydantic's artifact Requires-Dist spelling differs from
the original PyPI JSON declaration. Allocation 2 was not dispatched.

A bounded read-only observation of the 14 fixed artifact .metadata endpoints
recorded 246,306 bytes total. Both already retained wheel metadata entries match
those endpoint bytes exactly. Pydantic, Jinja2, Rich, markdown-it-py and Pygments
differ only in quotes, whitespace, parentheses or specifier order from the
preserved JSON declarations. No selected version, dependency or wheel changed.
The original wheel-inputs.json remains byte-for-byte intact.

wheel-metadata.json pins the actual metadata size, SHA256 and exact dependency
strings for every fixed wheel. The acquisition checks those metadata bytes inside
the SHA256-pinned archive, Name, Version, Requires-Python and exact Requires-Dist.
No dependency parser, installed package, normalization shortcut or dropped check
is introduced. Hash pinning establishes identity, not publisher authenticity.
