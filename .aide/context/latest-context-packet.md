# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: aide-lite
- generator_version: q14.token-ledger.v0
- contents_inline: false
- method: deterministic repo-local metadata, roles, priorities, and test heuristics

## SOURCE_REFS

- `.aide/context/compiler.yaml`
- `.aide/context/priority.yaml`
- `.aide/context/excerpt-policy.yaml`
- `.aide/context/ignore.yaml`
- `.aide/context/repo-snapshot.json`
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`

## REPO_MAP

- json: `.aide/context/repo-map.json`
- markdown: `.aide/context/repo-map.md`
- file_count: 641
- source_snapshot_hash: `f0f7696273b2cbfd97f1c0ed138fb6cfb4590a1142d9e622341129e961246519`

## ROLE_COUNTS

- aide_contract: 13
- aide_policy: 10
- aide_prompt: 3
- aide_context: 4
- aide_queue: 86
- aide_evidence: 100
- harness_code: 7
- compat_code: 5
- shared_code: 28
- test: 15
- docs: 261
- inventory: 11
- matrix: 6
- host: 37
- bridge: 8
- script: 6
- config: 38
- generated: 2
- unknown: 1

## TEST_MAP

- path: `.aide/context/test-map.json`
- mapping_count: 584
- mappings_with_existing_candidate: 571
- complete_coverage_claimed: false

## CURRENT_QUEUE

- current_queue_ref: `.aide/queue/Q14-token-ledger-savings-report/`
- queue_index: `.aide/queue/index.yaml`

## EXACT_REFS

- Preferred syntax: `path#Lstart-Lend`
- Validate refs before use.
- Do not inline whole files by default.
- Never inline ignored files, secrets, local state, caches, or binary artifacts.

## PACKET_GUIDANCE

- Use repo-map and test-map refs before broad documentation dumps.
- Include exact line refs only when required for correctness.
- Ask for additional context only when the compact packet is insufficient.

## TOKEN_ESTIMATE

- method: chars / 4, rounded up
- chars: 1893
- approx_tokens: 474
- formal ledger: `.aide/reports/token-ledger.jsonl`
