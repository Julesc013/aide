# Receipt baseline binding after independent delta review

## Rejected subject and independently confirmed overwrite

Independent reviewer `/root/owned_repair_integration_review` returned
`REQUEST_CHANGES` for commit
`3239530132a6d04c776dd0809392e0fd8f9dc322`, tree
`7fc61d7e944a81c4032a5040301ad6d4567f2c73`. External report:
`D:/Projects/AIDE/_review_scratch/three-way-32395301-independent-delta-review.md`,
SHA-256 `cc9c075fcb1e4f3543ae4ee5d375f24d57d1239003b2fa8dcb44ba3c0abddd48`.
Its two disposable AGENTS probes used a changed, checksum-valid incoming pack,
a directly edited CRLF managed block and a re-digested local receipt. With and
without the exact validated predecessor, preview said `update_owned`; apply
erased the edit. Both probe logs have SHA-256
`dbbab04d7036182eade14dd03ac0b8028dc5b29e8dc9031b78bb1d691f2fb5b4`.

The reviewer independently confirmed the analogous ordinary managed-file
overwrite, which predated the CRLF delta. Its external note is
`D:/Projects/AIDE/_review_scratch/three-way-32395301-managed-file-receipt-probe-note.md`,
SHA-256 `119dac2fff53468086e2198a4f93043252a9853c6fd66cd54eda4c793a0363f6`;
script SHA-256 `881e448ad4bcda7d44623e3e362bcde8eedae269ed659f742f7d9e76f55473e7`,
log SHA-256 `4db49d384e63a7d8f1d4340de345f4b91bf9afae361736a3af37e0e97491d449`.
The target was disposable. No repository or real consumer was changed by the
reviewer.

## Red oracle and repair

On exact source `32395301`, the extended AGENTS test failed both forged
receipt subtests (valid predecessor and absent predecessor): expected
`conflict`, observed `update_owned`. Exit 1; external log
`D:/Projects/AIDE/_review_scratch/three-way-forged-receipt-red-32395301.log`,
SHA-256 `e6bdd819916a6c3d26de7dcd1e314623d33436e99538a435f312ff5b165777e1`.
The ordinary managed-file red test failed the same two cases. Exit 1; log
`D:/Projects/AIDE/_review_scratch/three-way-forged-managed-red-32395301.log`,
SHA-256 `90b9f0f8eb4cd9f43a5ffb9c7988afe490e2c6d332fbc2a8143f0fcdc2c4d1a6`.

The repair allows automatic `update_owned` only when the supplied exact
predecessor passes pack validation and matches the receipt's pack identity,
then its payload proves the entry's source and installed baseline. An ordinary
managed file must match predecessor bytes exactly. A managed AGENTS section
may match only the predecessor block in its exact source, LF or CRLF rendering.
The observed target must still match the verified installed digest, ownership
must be `aide_portable_managed`, and a local overlay must be absent. With no
predecessor, changed upstream content conflicts and retains target bytes.
The portable guide and delivered install guide now state that the exact old
pack is required for an automatic update.

The focused three-test suite passed 3/3 in 158.269 seconds, exit 0, external
log `D:/Projects/AIDE/_review_scratch/three-way-predecessor-binding-green-focused.log`,
SHA-256 `720798dbb998bb1d65fd488e70aaff39795c10380fb8df51f19add8e49fd59aa`.
It includes ordinary owned update, v1/v2 CRLF survival and successive updates,
direct-edit overlay conflict, and both forged-receipt refusal classes. Exact
source SHA-256 `bad038a690d1c0a6cec3509c4722733cf39b9542c33738cc2f70fb12a3a4738b`;
test SHA-256 `2a425aa1997f5400138008c93c3d47022e5c5527ae9ef786b476c6277074aba9`.

The full importer suite began on those source/test hashes in external log
`D:/Projects/AIDE/_review_scratch/three-way-full-importer-predecessor-binding.log`.
Its exit and results were pending when this record was written. The prior
full-suite attempt on `32395301` was stopped on the security finding, exit 1,
zero-byte log SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
it is not passing evidence. Exact repaired-source review, artifact consumers,
replay and dev integration remain pending.
