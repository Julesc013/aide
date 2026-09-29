# Current ZIP host context canary repair

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.

Independent reviewer `/root/stable_effect_review` returned **REQUEST_CHANGES**
for commit `2d7671ed56008ef69bacc3486a78f508079e60e2`, tree
`d6eec838f3f010809665c074f7f98936378321d1`. The committed test selected
a user-specific Codex path and could hash different prompt bytes from those
sent to the debugger. The earlier D job remains a limited observation, not an
accepted dev integration subject.

Superseding source commit `a706e2e8cf296140fe3cf528d21f294d9646dbf2`,
tree `2e3ca17471a2ccc1f754ef7bb291156eb232a462`, takes the executable
path and expected SHA-256 from the ignored local job manifest. It reads at
most 4,097 prompt bytes once, rejects empty or over-limit content, and hashes
the same byte buffer sent to the debugger. The executable SHA-256 remains
`83751f15cb6a0a7b97df67752c001e3fe1c20e18ffbfec3ff63567296205eb6c`.

The ignored manifest SHA-256 was
`9563575ec8584c254faee3f7f5d6725fb97193e88638249b4b2898eb704e3c66`.
`job inspect` reported no active job, finite D reservation and no Codex model
admission. The exact run command was `py -3 .aide/scripts/aide_lite.py job run
--config .aide.local/execution.json --manifest
.aide.local/current-zip-host-context-job.json`.

Job `61a3bb4ac4e64c0797cb94653a981bf1` passed, exited zero and retired.
Manifest digest:
`5d2c4f7afccd8fa6cd0ebb7ef0d74b5b1a45be2e698e4de2bdb0ccbd5897168d`.
Receipt SHA-256:
`2865f238d09e198da7167ccf5097e4b950ee5a20532d35de98f8dbc4f8264c15`.
The sole output, `output/summary.json`, SHA-256
`0b79d8eec26447377aafb12773ff6d413bc27a4d76aa156a12079796d99bab15`,
reports the unchanged stable ZIP SHA-256 `27948415…`, delivered CLI SHA-256
`c15db586…`, prompt SHA-256 `d2dc3029…`, 756 prompt bytes, 23,093 debugger
JSON bytes and `COMPLETE` parsing of three messages with 21,928 visible UTF-8
bytes. It records zero model requests started by the parser and no actual
model turn. Effective tokens and tool definitions remain unknown. The raw
debugger JSON was piped in memory and was not retained in the bounded output.

Peak observed memory was 379,236,352 bytes; peak scratch was 1,609 bytes. The
job scratch path is absent and its reservation released. The stable ZIP was
not rebuilt. This evidence supports only the delivered CLI versus installed
host debugger context shape. Live turn usage, matched task quality/cost, main
promotion and publication remain separate gates.

Independent `/root/stable_effect_review` returned **ACCEPT for dev integration**
of exact source `a706e2e8cf296140fe3cf528d21f294d9646dbf2`, tree
`2e3ca17471a2ccc1f754ef7bb291156eb232a462`, after checking the repaired
diff, ignored local path/digest binding, bounded single prompt read and hashes
of the D rerun receipt and sole output. The reviewer closed both earlier
REQUEST_CHANGES findings. This is a scoped technical verdict on the no-model
debugger/parser canary; the reviewer did not run a live model turn or accept
release publication. This evidence closeout does not alter the reviewed source.

After report-only `git plan`, clean state, one registered worktree, four
passing new commit-message checks and exact remote `dev@f5512404` were
observed, local `dev` fast-forwarded to
`3cd57cb49620f7dadc15ebe207a6a90d25448e62`, tree
`579366cb5dacf46db004988b813365be2818a0cb`. A non-force push succeeded
and `git ls-remote` observed the same full `dev` object. Remote `main` stayed
`aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`; the stable ZIP SHA-256
remained `27948415530f260479c249b2d8cc956792eff4c77a524f0225f61f1f3f2ef7b1`.
This integration receipt is evidence-only and postdates the reviewed source.
