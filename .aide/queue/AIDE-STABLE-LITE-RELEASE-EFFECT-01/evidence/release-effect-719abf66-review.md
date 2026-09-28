# Superseding exact release-effect review

Independent `/root/stable_effect_review` returned **ACCEPT** for commit
`719abf66da58582e27206e1f1bdfc1fe3a26ef51`, tree
`8d4cacb300b1a8b019738d2a6f39d4f8bc518429`, against
`dev@a6725d83db101890f8734fcb52a3df1fe7091aa5`. The reviewed effect
manifest SHA-256 was
`b31addc4414967baecebd0405efc7726a522173fbbe1e2942f582fa939fd753a`.
The same independent reviewer subsequently confirmed that this was the CRLF
working-copy hash. The manifest in reviewed commit/tree has Git blob
`9983bf1dea84161ae84acee4dbd3d84adc12e027` and authoritative committed
LF SHA-256 `a42d1419e9103c295540a677f66163c1484eb466db354168f8d5297585997bff`.
Changing only its 623 LF endings to CRLF reproduces the earlier hash; JSON
content is identical and the reviewer explicitly retained **ACCEPT** for the
committed LF manifest. The signed clarification is preserved under the approved
D control root at `reviews/stable-effect-719abf66-lf-clarification.md`, SHA-256
`3386495bc2c75678b5d17582c29d71c84ccd5780841d1d19f0d7c3d126af64d5`.
The external review transcription remains under the approved D control root
at `reviews/stable-effect-719abf66-review.md`, SHA-256
`c170741da71dca1c72b4c5ace6decf6f55b189987541a6eae48d7b381e46cc19`.

The reviewer checked the policy hash, four asset hashes, ten current D job
receipts and exit/retirement/reservation state, and all 39 log hashes with
literal CLI form tokens and observed results. No heavy tests or external
effects were performed by the reviewer. The ACCEPT qualifies the delegated
dev/main/tag/publication sequence **subject to fresh mandatory gates**;
downloaded hashes and consumers remain postpublication obligations.

Subsequent `commit check --range main..dev` returned **FAIL** for ten other
undispositioned historical messages. The active promotion rule requires that
range check. This later finding blocks main/tag/publication despite the exact
release-effect ACCEPT; see the separate decision request in this task.
