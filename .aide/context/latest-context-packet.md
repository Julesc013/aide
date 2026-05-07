# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: aide-lite
- generator_version: q24.existing-tool-adapter-compiler.v0
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
- file_count: 1017
- source_snapshot_hash: `4611e2f0d7101bbc74b3463d5995917f281f4a285b8c4daad4c8e7108778b9fe`

## ROLE_COUNTS

- aide_contract: 38
- aide_policy: 36
- aide_prompt: 3
- aide_context: 4
- aide_queue: 141
- aide_evidence: 175
- harness_code: 7
- compat_code: 5
- shared_code: 28
- test: 43
- docs: 331
- inventory: 11
- matrix: 6
- host: 37
- bridge: 8
- script: 6
- config: 104
- generated: 11
- unknown: 23

## TEST_MAP

- path: `.aide/context/test-map.json`
- mapping_count: 876
- mappings_with_existing_candidate: 863
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
- chars: 1943
- approx_tokens: 486
- formal ledger: `.aide/reports/token-ledger.jsonl`
