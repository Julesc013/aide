# Q24 Prompt Summary

Implement Q24 Existing Tool Adapter Compiler v0 inside `julesc013/aide`.

Required outcome:

- compile concise AIDE token-survival, context, verifier, evidence, review,
  router/cache/local-state, export/import, Gateway no-call, and provider
  no-call guidance into generated or preview adapter outputs;
- support Codex/AGENTS, Claude Code, Aider, Cline, Continue, Cursor, Windsurf,
  and optional VS Code task previews;
- preserve manual content through managed sections;
- do not make generated adapter outputs canonical truth;
- do not call providers, models, networks, Gateway forwarding, external tools,
  or external repositories;
- add AIDE Lite adapter commands, tests, docs, generated previews, export-pack
  template inclusion, and evidence;
- stop at review.

This prompt depends on QFIX-01, QFIX-02, Q21, and preferably Q22/Q23 pilot
evidence if present. Q22/Q23 evidence is not present in this AIDE repo at Q24
start and must be recorded as a limitation rather than fabricated.
