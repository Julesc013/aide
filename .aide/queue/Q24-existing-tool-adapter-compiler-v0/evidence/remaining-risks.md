# Remaining Risks

- Q24 awaits independent review.
- Q22 and Q23 target-pilot evidence is now available in the sibling Eureka and
  Dominium repositories, but those queue items still await review in their
  target repos and are not canonical AIDE queue items.
- Eureka and Dominium pilots prove large target-repo task-packet reductions;
  they do not yet prove each generated adapter output has been consumed
  successfully by Codex, Claude Code, Aider, Cline, Continue, Cursor, or
  Windsurf in those repos.
- Existing tools may ignore generated guidance unless users explicitly point
  them at it.
- Generated guidance is advisory, not enforceable runtime policy.
- Non-AGENTS outputs remain preview-only and require future reviewed policy
  before root/tool writes.
- Tool-specific syntax and behavior may need adjustment after real target-repo
  use.
- Q24 does not implement actual IDE extensions, tool plugins, Gateway
  forwarding, MCP/A2A, provider calls, model calls, network calls, local model
  setup, Runtime, Service, Commander, UI, Mobile, semantic cache, exact
  tokenizer, provider billing, LLM-as-judge, automatic repair, or autonomous
  loops.
- Token savings remain estimated by AIDE Lite packet discipline, not exact
  provider billing truth.
- Adapter guidance must stay compact; future template growth could become a
  prompt-bloat regression and should be caught by review.
