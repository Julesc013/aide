# Context Compiler v0

## Purpose

Q11 adds the first deterministic AIDE Context Compiler. It reduces prompt size by turning repo state into compact metadata artifacts and context packets that reference paths, hashes, roles, likely tests, and optional line-range refs instead of inlining the whole repository.

## Commands

Run from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py context
py -3 .aide/scripts/aide_lite.py pack --task "Implement Q12 Verifier v0"
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Generated Artifacts

- `.aide/context/repo-map.json`: machine-readable file metadata, hashes, roles, priorities, and generated/manual classification.
- `.aide/context/repo-map.md`: compact human-readable role summary and important path list.
- `.aide/context/test-map.json`: heuristic source-to-test candidates with confidence, reason, and existence flags.
- `.aide/context/context-index.json`: generated artifact refs, counts, role counts, and source snapshot hash.
- `.aide/context/latest-context-packet.md`: compact context state packet for future prompts.
- `.aide/context/latest-task-packet.md`: regenerated compact task packet for the next phase.

These artifacts contain refs and metadata only. They do not inline raw source contents.

## Exact Refs

Preferred exact-reference syntax:

```text
path#Lstart-Lend
```

Q11 validates syntax and file bounds for text files. Full excerpt extraction remains deferred; whole-file inline is forbidden by default.

## Test Map Limits

The test map is heuristic. It uses path and naming conventions such as `core/harness/*.py` to `core/harness/tests/test_*.py`, `.aide/scripts/aide_lite.py` to `.aide/scripts/tests/test_aide_lite.py`, and structural Harness validation for docs/config. It does not claim complete coverage.

## Deferred Work

Embeddings, vector search, semantic cache, exact tokenizer support, token ledger formalization, Q12 verifier gates, provider billing, Gateway, routing, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, and autonomous loops remain deferred to later reviewed queue items.
