# Current ZIP and installed host context canary

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.
Test source commit `43c5e95e3186df19df87c629a92f0bf224f97433`, tree
`2a9b8c541f043e23bb9d1a3889cbdffc5e7c33ca`. The D job manifest file
`.aide.local/current-zip-host-context-job.json` had SHA-256
`eb66152d9f38eab2b334a517ea9d827062003f242d478809df9ad822e7694cce`.
The command was `py -3 .aide/scripts/aide_lite.py job run --config
.aide.local/execution.json --manifest
.aide.local/current-zip-host-context-job.json`.

Job `b55340cb07ae48db9dee12b93289f1ff` passed with manifest digest
`eca0295a4a2e0e2fa318387ac22c1e4a472885fc231647d8e5d23dbe66eb7df0`.
Retained receipt SHA-256:
`cd77641dc177829fd21fa71260534bc85646fd8d1fc864da176013bfe0c9a251`.
The sole retained output, `output/summary.json`, has SHA-256
`0b79d8eec26447377aafb12773ff6d413bc27a4d76aa156a12079796d99bab15`.
The source-bound ZIP SHA-256 was
`27948415530f260479c249b2d8cc956792eff4c77a524f0225f61f1f3f2ef7b1`;
the extracted CLI SHA-256 was
`c15db5864ba4d06ed64873bae035bf15d9832823b2e190b19c59477c9912ce04`.

The canary extracted only the CLI into a disposable consumer in admitted D
scratch. It ran the installed versioned `codex-cli 0.145.0` debugger with the
756-byte bound prompt, then sent its in-memory JSON directly to the **delivered
ZIP CLI** `job context` command. The delivered parser returned `COMPLETE`,
three messages, 23,093 debugger JSON bytes and 21,928 visible UTF-8 text
bytes: 18,308 developer and 3,620 user. It reported no content-shape gaps,
unknown effective tokens/tool definitions/internal inference and zero model
requests started by the parser. The result explicitly records no actual model
turn and no retained raw debugger JSON. The 1,397-byte summary contains no
task-prompt phrase; only one output file was retained.

The outer job exited zero, peak memory 379,166,720 bytes and peak scratch
1,609 bytes. The exact job scratch path is absent, the reservation was
released, and control has no active job. No new worktree or storage pool was
created. The source-checkout debugger view for the same prompt was 46,350
visible bytes; the lower consumer view reflects different loaded context,
not measured token savings or a quality result.

This closes a **no-model delivered-CLI/installed-debugger parser check**. It
does not qualify live `codex exec`, actual request usage or credits, the
effective future `--ignore-user-config` context, matched task quality/cost,
main promotion or publication. Seek independent technical review before
using this as release evidence. Local model permission remains absent.
