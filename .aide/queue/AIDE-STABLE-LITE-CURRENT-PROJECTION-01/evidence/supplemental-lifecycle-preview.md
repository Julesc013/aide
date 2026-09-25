# Supplemental local Windows lifecycle canary, 2026-09-25

- Exact locally generated ZIP SHA-256
  `68f8b3cc07c6476999828577c59bdb8785d13509613d0351a617908c99fa784c`,
  manifest source `0509e1611b1838c650954c64212ad603f132dada`.
- A copy of the previously reviewed external lifecycle canary changed only
  the ZIP path and expected SHA-256. Current script SHA-256
  `458291d6c6a078e7d65560f41e5cee762284fbb60e3fda4b8d2e14f7ebcd7f1c`;
  it retained the pinned extraction helper SHA-256
  `3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181`.
- Run exited 0/PASS with 31 delivered CLI invocations, 833 ZIP members,
  receipt-owned repair including wrong-plan/rival refusal and post-write
  recovery, exact-pack to synthetic-successor rollback, fresh and brownfield
  detach, and preservation-based partial removal. Summary SHA-256
  `621506d1551716a093b4b6be07e3ba8cad29927c1ac1efffbbb34cdb46e67ed4`;
  invocation log SHA-256
  `73d2880d2b208e63b59ab76f84129d7cfc205f8fd6cd86c2f16c75c4ae5e4f10`.
  All 31 command-log hashes and exit codes were independently recomputed by
  the controller: zero mismatches, seven expected nonzero refusals, no
  `failure.txt`; external `lifecycle-hash-audit.txt` SHA-256
  `3a7fe2f5a79de3ba4c89099748f110e20bfc225f53605c09c281a00ca2f6d778`.
- The focused dev-effect reviewer rehashed this supplemental summary/logs
  but did not rerun the canary. This is local preview evidence only. Its
  successor is synthetic; downloaded-byte acceptance, OS-level offline
  trace, hostile-process race and final stable profile remain open.
