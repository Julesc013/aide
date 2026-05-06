# AIDE Lite

## Purpose

AIDE Lite is the repo-local, no-install token-survival, context, verifier, review, token-ledger, golden-task, outcome-controller, and router helper introduced by Q09, hardened by Q10, extended by Q11, given mechanical verification in Q12, compact review-packet generation in Q13, estimated token accounting in Q14, deterministic local golden tasks in Q15, advisory outcome recommendations in Q16, and advisory route decisions in Q17. It prepares compact task packets, deterministic context snapshots, repo maps, test maps, context indexes, approximate token estimates, verifier reports, review packets, metadata-only token ledger records, savings summaries, golden-task reports, outcome reports, advisory recommendations, route-decision reports, managed agent guidance, and selftests without calling models, providers, network services, Gateway, Runtime, Service, Commander, hosts, or local model managers.

## Command Surface

Run commands from the repository root:

```bash
py -3 .aide/scripts/aide_lite.py doctor
py -3 .aide/scripts/aide_lite.py validate
py -3 .aide/scripts/aide_lite.py snapshot
py -3 .aide/scripts/aide_lite.py index
py -3 .aide/scripts/aide_lite.py context
py -3 .aide/scripts/aide_lite.py pack --task "Implement Q15 Golden Tasks v0"
py -3 .aide/scripts/aide_lite.py estimate --file .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py verify
py -3 .aide/scripts/aide_lite.py verify --task-packet .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py verify --review-packet .aide/context/latest-review-packet.md
py -3 .aide/scripts/aide_lite.py verify --changed-files
py -3 .aide/scripts/aide_lite.py review-pack
py -3 .aide/scripts/aide_lite.py ledger scan
py -3 .aide/scripts/aide_lite.py ledger report
py -3 .aide/scripts/aide_lite.py ledger compare --baseline root_history_baseline --file .aide/context/latest-task-packet.md
py -3 .aide/scripts/aide_lite.py eval list
py -3 .aide/scripts/aide_lite.py eval run
py -3 .aide/scripts/aide_lite.py eval report
py -3 .aide/scripts/aide_lite.py outcome report
py -3 .aide/scripts/aide_lite.py outcome add --phase Q16 --source validation --result PASS --failure-class unknown --severity info
py -3 .aide/scripts/aide_lite.py optimize suggest
py -3 .aide/scripts/aide_lite.py route list
py -3 .aide/scripts/aide_lite.py route validate
py -3 .aide/scripts/aide_lite.py route explain
py -3 .aide/scripts/aide_lite.py adapt
py -3 .aide/scripts/aide_lite.py selftest
```

Use `python` instead of `py -3` only when the Windows launcher is unavailable.

## Determinism Rules

- Generated text uses stable newlines and repo-relative paths.
- Snapshot records are sorted and include hashes, sizes, mtimes, extensions, coarse types, and summary counts, but no raw file contents.
- Repo-map and test-map records are sorted and contain metadata/refs only.
- `pack` writes `.aide/context/latest-task-packet.md` with context references and budget status instead of whole files.
- `verify` inspects packet shape, file refs, line refs, changed-file scope, adapter drift, context shape, token warnings, and obvious secret risks without raw file contents.
- `review-pack` writes `.aide/context/latest-review-packet.md` with task/context/verification/evidence refs, changed-file summaries, validation summaries, token summaries, risks, and decision instructions without full diffs or source dumps.
- `ledger scan` and `ledger report` write metadata-only estimated token records and compact savings summaries without raw prompts or raw responses.
- `eval list`, `eval run`, and `eval report` run Q15 deterministic local golden tasks and write metadata-only PASS/WARN/FAIL reports.
- `outcome report` writes `.aide/controller/latest-outcome-report.md` and `.aide/controller/outcome-ledger.jsonl` from deterministic local token, verifier, review, context, eval, and adapter signals.
- `optimize suggest` writes `.aide/controller/latest-recommendations.md` with evidence sources, expected benefits, risk levels, next actions, rollback conditions, and `applies_automatically: false`.
- `route list` prints advisory route classes, task profiles, and hard floors without provider calls.
- `route validate` checks Q17 routing policy/model files, hard floors, route-decision shape, and live-call-disabled posture.
- `route explain` writes `.aide/routing/latest-route-decision.json` and `.aide/routing/latest-route-decision.md` with task class, risk class, route class, hard floor, quality gates, evidence sources, and advisory-only safety status.
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

AIDE Lite does not implement exact tokenization, provider billing integration, real API usage accounting, automatic GPT review calls, live routing, route execution, cache sharing, Gateway, provider adapters, Runtime, Service, Commander, UI, Mobile, MCP/A2A, host behavior, embeddings, vector search, semantic cache, LLM-as-judge, automatic repair, autonomous loops, or automatic prompt/policy/route mutation.
