# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: aide-lite
- generator_version: q12.verifier.v0
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
- file_count: 613
- source_snapshot_hash: `d208e4f2255fb36b61cc63f63ae2fc2d172c4f5926315e42c8a23a0476eaf966`

## ROLE_COUNTS

- aide_contract: 13
- aide_policy: 9
- aide_prompt: 3
- aide_context: 4
- aide_queue: 78
- aide_evidence: 89
- harness_code: 7
- compat_code: 5
- shared_code: 28
- test: 13
- docs: 258
- inventory: 11
- matrix: 6
- host: 37
- bridge: 8
- script: 6
- config: 36
- generated: 2

## TEST_MAP

- path: `.aide/context/test-map.json`
- mapping_count: 559
- mappings_with_existing_candidate: 546
- complete_coverage_claimed: false

## CURRENT_QUEUE

- current_queue_ref: `.aide/queue/Q11-context-compiler-v0/`
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
- chars: 1847
- approx_tokens: 462
- formal ledger: deferred to Q14
