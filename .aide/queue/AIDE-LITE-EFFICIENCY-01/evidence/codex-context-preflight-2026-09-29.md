# Codex host context preflight — no model turn

Date: 2026-09-29. Working root: the AIDE source checkout at `dev@47b0883bb87b38cc9a7d8899090e46a24c85aabf`.

The installed `codex.exe` was `codex-cli 0.145.0`, SHA-256 `83751f15cb6a0a7b97df67752c001e3fe1c20e18ffbfec3ff63567296205eb6c`. A local `codex debug prompt-input` call disabled apps, hooks, multi-agent and remote plugins through process-local `-c` options and appended only the fixed 44-byte probe message. It exited zero without starting a model turn. A bounded local parser read 47091 JSON output bytes and retained **only counts**, not prompt text:

| Role | Messages | Parts | Visible text UTF-8 bytes |
| --- | ---: | ---: | ---: |
| Developer | 1 | 3 | 21834 |
| User | 2 | 3 | 23805 |
| **Total** | **3** | **6** | **45639** |

This is a fresh local debugger view, not the current long-lived thread, a token count, an authenticated live worker effect, or a full model request. Tool definitions and internal inference were not measured. The local host's base visible text substantially exceeds the 44-byte probe; a small task packet alone therefore cannot establish a small effective context. Raw prompt contents were neither printed nor committed. A version-qualified admitted host binding, actual usage coverage and matched quality/cost comparison remain open.
