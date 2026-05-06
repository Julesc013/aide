# AIDE Lite

## Purpose

AIDE Lite is the repo-local, no-install token-survival helper introduced by Q09 and hardened by Q10. It prepares compact task packets, deterministic context snapshots, approximate token estimates, managed agent guidance, and selftests without calling models, providers, network services, Gateway, Runtime, Service, Commander, hosts, or local model managers.

## Command Surface

Run commands from the repository root:

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

## Determinism Rules

- Generated text uses stable newlines and repo-relative paths.
- Snapshot records are sorted and include hashes, sizes, mtimes, extensions, coarse types, and summary counts, but no raw file contents.
- `pack` writes `.aide/context/latest-task-packet.md` with context references and budget status instead of whole files.
- `adapt` preserves manual `AGENTS.md` content outside managed markers and can run twice without changing the file.
- Managed-section drift is reported by `doctor` or `validate` and repaired by `adapt` because the section is generated.

## Validation And Tests

Use both command-level selftests and unittest discovery:

```bash
py -3 .aide/scripts/aide_lite.py selftest
py -3 -m unittest discover -s .aide/scripts/tests
py -3 -m unittest discover -s core/harness/tests -t .
```

The direct `.aide/scripts/tests` discovery form is the supported Q10 shape. Python's `-t .` top-level discovery form can fail on hidden `.aide` package naming, so Q10 records that as a discovery limitation rather than moving the no-install tests out of `.aide/scripts/tests`.

## Deferred Work

AIDE Lite does not implement exact tokenization, provider billing, a token ledger, the full Q11 context compiler, Q12 verifier, Q15 golden tasks, routing, cache sharing, Gateway, provider adapters, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, or autonomous loops.
