# AIDE Latest Context Packet

## CONTEXT_COMPILER

- compiler: q11-context-compiler-v0
- generator: aide-lite
- generator_version: q13.evidence-review.v0
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
- file_count: 625
- source_snapshot_hash: `b0038c793799295dc5f6a1715dbbf6e8354f8a881b8f138926c079f65d1eca26`

## ROLE_COUNTS

- aide_contract: 13
- aide_policy: 9
- aide_prompt: 3
- aide_context: 4
- aide_queue: 82
- aide_evidence: 94
- harness_code: 7
- compat_code: 5
- shared_code: 28
- test: 14
- docs: 259
- inventory: 11
- matrix: 6
- host: 37
- bridge: 8
- script: 6
- config: 37
- generated: 2

## TEST_MAP

- path: `.aide/context/test-map.json`
- mapping_count: 570
- mappings_with_existing_candidate: 557
- complete_coverage_claimed: false

## CURRENT_QUEUE

- current_queue_ref: `.aide/queue/Q13-evidence-review-workflow/`
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
- chars: 1859
- approx_tokens: 465
- formal ledger: deferred to Q14
