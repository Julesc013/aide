# Token Survival Core

## Purpose

Q09 adds the first repo-only token-survival layer for AIDE. Q10 hardens its no-install AIDE Lite workflow so future Codex and GPT-5.5 work can start from compact repo-derived packets instead of long chat history.

## Commands

Run these from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py pack --task "Implement Q11 Context Compiler v0"
py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py adapt
py -3 .aide/scripts/aide_lite.py selftest
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Operating Rule

Future implementation prompts should use `.aide/context/latest-task-packet.md` as the starting packet. Agents should not paste prior full chat transcripts, whole repo dumps, repeated roadmap dumps, or full files unless exact file contents are explicitly needed.

## Q10 Hardening

Q10 keeps AIDE Lite standard-library only and makes it importable for tests. The helper now reports adapter drift, writes deterministic managed sections, avoids rewriting unchanged generated outputs, refuses binary-like estimates, adds snapshot summaries, warns when compact packets exceed configured budgets, and preserves manual `AGENTS.md` content outside managed markers.

Run the direct tests with:

```bash
py -3 -m unittest discover -s .aide/scripts/tests
```

Python discovery with `-s .aide/scripts/tests -t .` is awkward because `.aide` is a hidden directory name rather than a normal import package; Q10 records that as a test-discovery limitation while keeping the test module runnable through the direct start directory.

## Quality Rule

Token reduction is not accepted if it reduces correctness, provenance, rationale, durable memory, auditability, or review gates. Q09/Q10 use approximate `chars / 4` token counts only; exact tokenizer and provider billing integration are deferred.

## Deferred Work

Gateway, provider routing, cache sharing, local model setup, Runtime, Service, Commander, Mobile, MCP/A2A, semantic cache, vector search, Q11 context compilation beyond snapshot refs, and autonomous maintenance remain deferred until later reviewed queue items.
