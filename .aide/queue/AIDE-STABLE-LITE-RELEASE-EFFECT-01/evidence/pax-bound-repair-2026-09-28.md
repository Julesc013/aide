# PAX pre-parse resource bound repair

The second independent REQUEST_CHANGES found that yielded-member limits could
not bound tar PAX metadata parsing. The repair supplies a tarinfo class that
rejects PAX/GNU metadata declarations over 1 MiB before the parser reads
them, rejects GNU sparse metadata, and wraps decompressed tar reads in a
640 MiB cumulative bound. The existing 128 MiB compressed-file, 10,000-member
and 512 MiB regular-content limits remain. A tiny crafted PAX archive verifies
refusal before `_proc_pax`; the complete valid Q47/Q48 suite verifies normal
archives still work. This is bounded application validation, not an OS memory
sandbox.

Code SHA-256: `bf60d2a094f65e2fd75b028193f3df7dbbf253446f14a8910ab974dd3e963949`.
Q47 test SHA-256: `421faa6ce8ed45d04493f681a850c3fc218b70233b53527140d3b1aea86ecdf0`.

Configured D: managed runner:

- Focused job `f9fca29be5464d19b5fb1a7897688c41`: three tests passed,
  exit 0, scratch retired and reservation released. Receipt SHA-256
  `5c2bd2be0f5998ba9d49b421c241b98d302422ce3d3c7295a1ffac860dbfe576`.
- Full job `6749b91a0de0482897b651bbb1916e5b`: 36 Q47/Q48 tests passed in
  62.014 seconds, exit 0. Peak memory 271,245,312 bytes; peak scratch
  5,411,978 bytes. Scratch retired and reservation released. Receipt SHA-256
  `7a565f1326c11b696759fa013e0207fa58bd257af9f4a07e797b0aced3ea7e90`.

Final D manifest SHA-256:
`87b7f1f2e028397a10edffe8999934d5e9a5c60a174ebcdee1e8a3eb71125d84`.
The dirty repair ran atop `34c87052`; exact code and test hashes bind this
evidence. Freeze a new commit for independent review. Final assets, consumer
bytes and publication remain unqualified.
