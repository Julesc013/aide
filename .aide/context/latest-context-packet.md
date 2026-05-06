# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: aide-lite
- generator_version: q18.cache-local-state-boundary.v0
- contents_inline: false
- method: deterministic repo-local metadata, roles, priorities, and test heuristics

## SOURCE_REFS

- `.aide/context/compiler.yaml`
- `.aide/context/priority.yaml`
- `.aide/context/excerpt-policy.yaml`
- `.aide/context/ignore.yaml`
- `.aide/context/repo-snapshot.json`
- `.aide/context/context-index.json`
- `.aide/memory/project-state.md`
- `.aide/memory/decisions.md`
- `.aide/memory/open-risks.md`

## REPO_MAP

- json: `.aide/context/repo-map.json`
- markdown: `.aide/context/repo-map.md`
- file_count: 738
- source_snapshot_hash: `40ba0dbef9b3e3d77506333d110013f3fe7d2811e42fe2a419d66addf0d561a7`

## ROLE_COUNTS

- aide_contract: 30
- aide_policy: 32
- aide_prompt: 3
- aide_context: 4
- aide_queue: 102
- aide_evidence: 124
- harness_code: 7
- compat_code: 5
- shared_code: 28
- test: 19
- docs: 271
- inventory: 11
- matrix: 6
- host: 37
- bridge: 8
- script: 6
- config: 40
- generated: 2
- unknown: 3

## TEST_MAP

- path: `.aide/context/test-map.json`
- mapping_count: 665
- mappings_with_existing_candidate: 652
- complete_coverage_claimed: false

## CURRENT_QUEUE

- current_queue_ref: `.aide/queue/Q17-router-profile-v0/`
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
- chars: 1935
- approx_tokens: 484
- formal ledger: `.aide/reports/token-ledger.jsonl`
