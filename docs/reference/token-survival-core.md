# Token Survival Core

## Purpose

Q09 adds the first repo-only token-survival layer for AIDE. It exists so future Codex and GPT-5.5 work can start from compact repo-derived packets instead of long chat history.

## Commands

Run these from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py pack --task "Implement Q10 AIDE Lite hardening"
py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py adapt
py -3 .aide/scripts/aide_lite.py selftest
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Operating Rule

Future implementation prompts should use `.aide/context/latest-task-packet.md` as the starting packet. Agents should not paste prior full chat transcripts, whole repo dumps, repeated roadmap dumps, or full files unless exact file contents are explicitly needed.

## Quality Rule

Token reduction is not accepted if it reduces correctness, provenance, rationale, durable memory, auditability, or review gates. Q09 uses approximate `chars / 4` token counts only; exact tokenizer and provider billing integration are deferred.

## Deferred Work

Gateway, provider routing, cache sharing, local model setup, Runtime, Service, Commander, Mobile, MCP/A2A, semantic cache, vector search, and autonomous maintenance remain deferred until later reviewed queue items.
