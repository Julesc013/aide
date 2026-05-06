# Q20 Remaining Risks

- Q20 is not a live provider adapter.
- Provider capabilities are conservative metadata, not measured performance or availability evidence.
- No provider probes run.
- No credentials are configured.
- No pricing, billing, quota, or usage data is measured.
- No local model setup or download exists.
- No OpenAI-compatible or Anthropic-compatible forwarding exists.
- No provider response cache exists.
- No exact tokenizer exists.
- No Gateway forwarding exists.
- No MCP/A2A exists.
- Route decisions remain advisory and local.
- Gateway status remains local/report-only.
- `.aide.local/` is the future credential/local-state boundary, but Q20 does not create real local state.
- Direct unittest discovery under hidden `.aide/scripts/tests` remains a known Python importability limitation in this repository; direct test files and AIDE Lite selftest pass.
- Generated manifest/review-gate nuance from earlier phases remains visible where it already existed.

## Next Recommended Phase

Q21 Existing Tool Adapter Compiler v0 should compile metadata for existing
deterministic tool adapters without enabling provider execution, live model
calls, Gateway forwarding, credentials, or runtime/UI behavior.
