# Current-source live-host readiness boundary

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.
Current source: `dev@9bef74f12f1acbefe09ded3a6b5a1a0104fad9c0`, tree
`5fb25073d91d5bac34a86acf75ffa90f33711545` before this evidence record.

The existing D-managed local configuration has no `codex_exec` model permission.
The controller prepared one ignored local, read-only `codex_exec` job for a
bounded review of AIDE's pause-before-resume invariant. It binds model
`gpt-6-sol`, effort `medium`, the current source commit/tree, a prompt, JSON
result schema and two exact source files. The prompt, schema and job JSON
SHA-256 values are respectively:

- `0461fe712a0ffc1ffc2c173268b93e31091487af46cb531206a15e48e5a0404e`
- `f3c3c1aa06e89b695ab36f1d518b572154f1bc72f257f055356bd2bcbbfcea91`
- `665a2821d3e695852396399e98908d8c3b72be5f95d6f44e03cf22d051f05a30`

The default installed `codex.exe` launcher traverses the `Codex\\bin`
junction and correctly failed AIDE's ordinary-executable-path guard. The
existing versioned executable at
`C:\Users\Jules\.codex\packages\standalone\releases\0.145.0-x86_64-pc-windows-msvc\bin\codex.exe`
has no reparse ancestor. It reports `codex-cli 0.145.0`, SHA-256
`83751f15cb6a0a7b97df67752c001e3fe1c20e18ffbfec3ff63567296205eb6c`,
the same bytes as the junction launcher. Its read-only `exec --help` exposes
the adapter's required options, including `--ephemeral`, `--ignore-user-config`,
`--output-schema`, `--json`, `--cd`, `--sandbox` and `--model`. No binary was
copied or configuration changed to resolve the path.

`py -3 .aide/scripts/aide_lite.py job inspect --config .aide.local/execution.json
--manifest .aide.local/efficiency-live-host-job.json` returned structured
`REFUSED`, reason `Codex job has no matching local model permission`,
`writes: false`. The local configuration SHA-256 remained
`73c0b1a4f4bb7cf341c8882806852a9aaea81c81a3d956cde575c1814e3616f6`.
At observation time, the shared control root had no dispatch record, the D
scratch root had zero children, and no model turn was launched.

This is a prepared and refused admission check, not live host qualification or
proof of effective context, actual usage or matched quality/cost. A separate
explicit local permission for one ChatGPT `gpt-6-sol`/`medium` turn is pending.
If granted, recheck current source/input/executable hashes, storage capacity,
dispatch epoch and authentication immediately before the one turn. If denied
or unavailable, retain this exact blocker and continue only independent work.
