# Q10 AIDE Lite Hardening Evidence

## Command Surface Before

Q09 created `.aide/scripts/aide_lite.py` with repo-local `doctor`, `validate`, `estimate`, `snapshot`, `pack`, `adapt`, and `selftest` commands. The Q09 surface could generate compact packets, but it was still intentionally shallow:

- adapter guidance used legacy Q09 markers;
- `pack` was Q10-oriented rather than generic enough for Q11+;
- validation did not check latest task-packet sections, budget overflow, adapter drift, or review-packet size;
- snapshot generation recorded file metadata but no summary counts;
- writes were not no-op aware;
- tests lived only under `core/harness/tests` because direct `.aide/scripts/tests` coverage had not been added.

## Command Surface After

Q10 keeps the same stable required commands and adds optional `version` and `show-config` helpers:

- `doctor`: reports repo root, Q09/Q10 readiness, required files, snapshot/latest-packet presence, adapter drift/current status, and validation posture.
- `validate`: checks token-survival required files, prompt sections, token-budget anchors, context exclusions, project-state budget, latest task-packet sections/budget, review-packet budget when present, AGENTS managed-section status, and obvious secret patterns.
- `estimate --file PATH`: reports path, chars, lines, and approximate tokens; missing files and binary-like files fail clearly.
- `snapshot`: writes sorted metadata records with hashes, sizes, mtimes, extensions, coarse types, and summary counts; no raw file contents are stored.
- `pack --task TEXT`: writes `.aide/context/latest-task-packet.md` for the requested task using context refs, output schema, evidence requirements, and budget status.
- `adapt`: preserves manual `AGENTS.md` content, replaces only the managed token-survival section, migrates legacy Q09 markers, and reports before/after adapter status.
- `selftest`: exercises deterministic internal behavior without provider, model, network, or external worker calls.

## Implementation Choices

- The helper is importable and has no CLI side effects unless `main()` is invoked.
- Core behavior is split into pure helpers for repo-root handling, token estimates, ignore matching, snapshot collection, deterministic writes, packet rendering, managed-section status, adapter replacement, validation checks, and selftests.
- Deterministic writes normalize line endings, preserve manual content outside managed markers, and avoid rewriting unchanged files.
- The generated token-survival section uses `AIDE-GENERATED` markers aligned with existing managed-section conventions.
- Legacy Q09 token-survival markers are replaced because they are managed output; manual AGENTS content is preserved.
- Packet rendering infers a phase id from task text such as `Q11` and references repo state instead of inlining source files.
- Budget enforcement remains warning-oriented for Q10 so ordinary operation is not blocked while Q14 ledger work is still deferred.

## Drift Behavior

- Missing managed section: `adapt` appends it.
- Current managed section: `adapt` reports `unchanged`.
- Legacy Q09 managed section: `adapt` replaces it with Q10 generated markers.
- Drifted Q10 managed section: `adapt` replaces only the managed body.
- Manual content outside markers is preserved.

## Scope Boundaries Preserved

Q10 does not implement Gateway, live model routing, provider calls, local model setup, exact tokenizer, provider billing ledger, full context compiler, full verifier, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host/app behavior, or autonomous loops.
