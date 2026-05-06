# Q09 Remaining Risks

- Q09 awaits independent review and is not marked passed.
- Generated manifest drift was present before Q09; final validation reports the manifest current because Q09 refreshed it through `py -3 scripts/aide compile --write`.
- Stale generated outputs can recur when generated-artifact source inputs change.
- Q00-Q03 and Q05/Q06 raw queue status nuance remains unresolved and intentionally visible.
- Token counts are approximate `ceil(chars / 4)` estimates only.
- No exact tokenizer or provider billing ledger exists yet.
- No live provider billing integration exists yet.
- No context compiler beyond metadata snapshot exists yet.
- No verifier/evidence gate beyond Q09 basics exists yet.
- No `.aide.local` local-state/cache boundary exists yet.
- No golden task quality proof exists yet.
- No Gateway, provider router, cache sharing, Runtime, Service, Commander, Mobile, MCP/A2A, host implementation, or autonomous maintenance loop exists yet.
- The requested `.aide/scripts/tests` unittest discovery shape with `-t .` is not viable because Python treats hidden `.aide` as a non-importable module path; Q09 tests live under `core/harness/tests` instead.
