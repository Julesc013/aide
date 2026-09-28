# Reviewed artifact and observed dev effect, 2026-09-28

Exact reviewed candidate `e7c1760e8e5b1031293ae5e54cfd266489fa805b`,
tree `ff4bbfaf17d084500093a327ae862df70595da91`, descends from
`dev@1d3d9fe1bb517bb8b9ce18cd26901a00dc9c4c30`. The final four
D-managed release commands bound that exact commit/tree, exited zero, retired
scratch, released reservations and changed **zero** tracked or untracked
paths. External result JSONL SHA-256:
`f68f641feb9a0c71ca1bc1426d4575e9a75752e658b8097e0523d12e0f3e59c7`.
`pack-status` returned `PASS_SOURCE_ANCESTOR` with valid checksum/boundary.
The five-commit AIDE message range from the prior dev passed.

Independent `/root/partial_artifact_review` (GPT-6 Sol) performed read-only
inspection and returned **ACCEPT_WITH_NOTES** for local dev fast-forward only.
The exact controller transcription under D control is
`reviews/partial-recovery-artifact-e7c1760e-review.md`, SHA-256
`3cd6a959576abd384de88fd3bbd56c20e7b4a60f0dc84716fa43460be19d8746`.
The reviewer did not run tests or remote checks. Its note permits the exact
external replay receipt as dev-effect evidence and requires observed effect
recording; stable publication was explicitly outside the verdict.

Before mutation the task worktree and other registered checkout were clean,
no managed D job or common Git lock was observed, local and remote dev both
read `1d3d9fe1`, the helper plan was ready_dry_run, and ancestry held. Under
authenticated `BLACKGLASS-WIN1\Jules` / `Julesc013`, local dev was advanced
atomically with expected old ref, then pushed normally without force. Local
and remote dev both read back `e7c1760e8e5b1031293ae5e54cfd266489fa805b`,
tree `ff4bbfaf17d084500093a327ae862df70595da91`.

The ZIP SHA-256 remains
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`;
tar.gz SHA-256 remains
`f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725`.
This follow-up changes only queue/evidence state. It does not amend the
reviewed source/artifact candidate or turn preview assets into a stable
release. Main remains `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`;
no tag or public release effect was performed.
