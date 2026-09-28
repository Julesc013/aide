# Dev integration and current-byte public CLI canary — 2026-09-28

Independent reviewer `/root/runner_repair_review` accepted source candidate
`cf0c4434f26020a50c8fbccd8ef6251470861504`, tree
`5cfdd62d194a261e007b4b8d34e92da6f7e297ee`, with notes for dev only.
The task branch also contains admission `b7492319` and evidence-only review
closeout `b7f595424f0497f79b9cf56414186fb70a82d553`, tree
`59dec226d3b93167acc1ecd2b54cfceaeaa214e2`. AIDE's three-commit
message range and `git diff --check` passed; the working tree was clean.
Local `dev` was atomically fast-forwarded from
`33abef7fca1547de6a3ca6de54ef0b99bedc6ef1` to `b7f59542`, then
normally pushed. `git ls-remote` observed origin/dev at the exact same full
commit. Origin/main remained
`aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.

The frozen local preview ZIP remains SHA-256
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`.
Its delivered public CLI canary ran in D job
`b7fcfc90c8734a82b0c16dc2b77dcf52`, manifest SHA-256
`07390d52d1b5b5cbc87b89dd0ce91273f1957703280d689137d26a851571c`,
ignored local oracle SHA-256
`384fc39e550fddf238a10ca7c123e7bea6532908da7a57203da45cd0eabac72e`.
It extracted 834 regular members and installed into a disposable fresh target.
An ordinary dry run created no feedback; explicit `--dry-run --explain
--feedback-out` created a local `manual_only` packet with `network_calls=false`,
four digest-bound explanations and unknown project rationale. Requesting
feedback without dry run exited one and created no packet. Project-owned and
installed source bytes were unchanged by these previews. Child exit zero;
peak scratch 8,180,370 bytes, peak memory 213,053,440 bytes; scratch retired
and reservation released. Summary SHA-256
`a9c5f285fe7c6a84bb45e75045d3c82787355ad9b567d9579e74bc3750776f22`;
receipt SHA-256
`4e8662e232def52c12a5b2ba03ce0b930555fc939d3adf73f9b42f63d1400573`.

This is local preview evidence. It does not establish OS-level native offline
traffic, every candidate public CLI form, final frozen version/profile,
release ACCEPT, main promotion, tag/publication or downloaded-byte consumers.
