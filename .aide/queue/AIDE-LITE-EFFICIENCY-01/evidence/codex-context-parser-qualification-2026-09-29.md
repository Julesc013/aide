# Portable Codex context parser: source qualification

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.

Source candidate `b4f250f7bc9f7411f00b7387736542ce128ce199`, tree `6a4b3bfd09a3453b249fe03a930bddd4e916031b`, extends the existing Lite `job` CLI with read-only `job context`. It accepts one Codex `debug prompt-input` JSON stream on stdin, caps input at 2 MiB and shape at 128 messages/32 parts each, counts visible text by role, and prints no supplied text. Unknown roles or non-text parts are `PARTIAL`; tokens, tool definitions and internal inference remain unknown. The parser starts no model request.

The first frozen source `6f4b45a6` passed synthetic cases but failed its installed-host assertion: the real stream uses `input_text`. The second `1340ecd8` still counted zero visible bytes. Those failed D-managed attempts are retained as jobs `8d1a940e736545d29638aa1993da02d5` and `60d10e2955d648dba6d20ccf79079c1f`; neither is relabelled successful. A sanitized-environment read-only schema inspection exposed `input_text` in all six real content parts. `b4f250f7` fixed the parser and its oracle.

The superseding exact source passed **3/3** focused cases in D-managed job `4d695169668f445ca2a9ba799bc5252e` (`python -m unittest discover -s .aide/scripts/tests -p test_efficiency_wait.py -k prompt_input -v`). Its installed Codex debugger result was `COMPLETE`, three messages, 45728 visible UTF-8 text bytes, no content gaps. The retained receipt SHA-256 is `5430f6f07a80f4a66d927f4349bf4836111938bae248653c7cd29e99a59accde`; exit 0, peak memory 262860800 bytes, peak scratch 871 bytes, scratch absent and reservation released. No raw prompt content was printed or committed.

Independent `/root/stable_effect_review` returned **ACCEPT for dev source integration** of `b4f250f7` and independently verified the receipt and cleanup. The reviewer requires a `job context` assertion in the next extracted-pack/artifact qualification; source-level CLI and installed-host checks do not prove new delivered bytes. This verdict does not qualify a live Codex turn, complete effective context, token cost, stable release or publication.
