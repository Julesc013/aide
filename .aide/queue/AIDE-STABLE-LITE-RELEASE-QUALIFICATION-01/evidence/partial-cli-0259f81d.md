# Delivered public partial recovery and predecessor feedback — 2026-09-28

Source `0259f81d8fca993b27781540ebc3f70b0c6fedcb`, tree
`0fb6e798e10a225cf9efed5f4689bb1ca1aae108`, used the unchanged local
preview ZIP SHA-256
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`
and tar SHA-256
`f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725`.
The archive pair had 834 matching regular members and delivered CLI SHA-256
`25829e62e404a78c8fd053d3917909381cb9d31785a1df6af86370895e87451c`.

The first D job `0111001fe88c4e72a6dfc672d9c59716` passed six public CLI
recovery checks for disposable fresh import and predecessor update. A direct
delivered-module fault hook created a genuine partial payload state in each
case. Ordinary retry and wrong-plan `--recover-partial` both returned
`RECOVERY_REQUIRED`; `--recover-partial --expect-plan <original digest>` from
the delivered CLI returned `RECOVERED`. Project-owned bytes survived, the
successor receipt matched the synthetic pack, and active intent retired.
Its child exited zero and scratch/reservation retired. The second job extends
that same oracle and supersedes it for the final result below.

Final D job `70551c019984482bb8176cef56a91c86` passed seven public CLI
checks. Between fresh recovery and partial update, the predecessor-bound
`--dry-run --explain --feedback-out` form returned `PLANNED` and produced
six digest-bound explanations in a local `manual_only` packet with
`network_calls=false`. No feedback existed before explicit opt-in, and the
preview preserved project-owned bytes. Both subsequent partial recovery paths
again reached `RECOVERED`. The synthetic successor is **not published**.
Child exit zero; peak scratch 16,063,992 bytes, peak memory 298,414,080 bytes;
scratch retired and reservation released. Final ignored oracle SHA-256
`88c1cdae6110f632838a321b5177db39fb988121f961da78fbe2da6aa802c1bd`;
manifest SHA-256
`17dd7ec53826fbd9ff0e490315e85008e4eea698754597f009b22652520daefa`;
summary SHA-256
`6612e934f493fc7ba8477190d96aef31c63ef36b81253f7601dc1062e44cbf4f`;
retained receipt SHA-256
`3f301c4f3e1a728e517b5b5b0699b84a1af9e844e2f66c9132532620d94ae3d0`.

These are current local preview and fixture-predecessor results, not a
published predecessor matrix or downloaded-byte proof.

After the seven-command result, a final ten-command D job
`b2819789ccd5463182478fd1516e28f1` added a project-selected resolution
case. A disposable V3 upstream change conflicted with a direct target edit;
the saved exact plan partially applied. Ordinary retry and recovery with a
changed resolution file returned `RECOVERY_REQUIRED`; restoring the original
resolution and using the installed `--resolve <target-path>
<resolution-file> --recover-partial --expect-plan <digest>` returned
`RECOVERED`. The selected bytes and project-owned file survived; active intent
retired. Fresh and ordinary predecessor recovery plus opt-in predecessor
feedback also passed again. Synthetic V2/V3 remain unpublished fixtures.
Child exit zero; peak scratch 20,464,355 bytes, peak memory 298,610,688 bytes;
scratch retired and reservation released. Final oracle SHA-256
`a1fbff1147cdf341e00da4a5c40869cdccd1dd2011dbc20dbcbff9db6f64456d`;
manifest SHA-256
`061c327f6a65be95c4959c1fb208f347bbe6700a5f71d4220cedeb37d3e3c3e8`;
summary SHA-256
`deba61c43c066b278c4d5feb78f7538f37b8a948990c089eeeebe0283ca5991b`;
retained receipt SHA-256
`60b14ce8a60496b07552070987eb7577d06dbcb6349f98f945d2a220c0f2af00`.
This supersedes the seven-command result for public resolved recovery.
