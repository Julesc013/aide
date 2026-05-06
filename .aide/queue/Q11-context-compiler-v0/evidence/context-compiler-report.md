# Q11 Context Compiler Report

## Generated Context Artifacts

- `.aide/context/compiler.yaml`: context compiler policy/config.
- `.aide/context/priority.yaml`: context family priority rules.
- `.aide/context/excerpt-policy.yaml`: no-full-file and line-ref policy.
- `.aide/context/repo-map.json`: machine-readable repo map.
- `.aide/context/repo-map.md`: compact human-readable repo map.
- `.aide/context/test-map.json`: heuristic source-to-test map.
- `.aide/context/context-index.json`: generated artifact refs and counts.
- `.aide/context/latest-context-packet.md`: compact context packet.
- `.aide/context/latest-task-packet.md`: regenerated Q12 task packet.

## Counts

- repo-map file count: 594
- test-map mappings: 542
- test-map mappings with existing candidate: 529
- latest context packet: 1,855 chars, 464 approximate tokens
- latest Q12 task packet: 2,942 chars, 736 approximate tokens

## Role Categories

- aide_context: 4
- aide_contract: 13
- aide_evidence: 84
- aide_policy: 8
- aide_prompt: 3
- aide_queue: 74
- bridge: 8
- compat_code: 5
- config: 33
- docs: 254
- generated: 2
- harness_code: 7
- host: 37
- inventory: 11
- matrix: 6
- script: 6
- shared_code: 28
- test: 11

## Ignored Path Behavior

The compiler uses `.aide/context/ignore.yaml` and excludes `.git/**`, `.env`, `.aide.local/**`, caches, `node_modules/**`, `dist/**`, `build/**`, binary/media/archive patterns, and generated context outputs from snapshot/map records. Validation checks that ignored paths do not appear in `repo-map.json`.

## Test Map Behavior

The test map is heuristic and does not claim complete coverage. Examples:

- `.aide/scripts/aide_lite.py` maps with high confidence to `.aide/scripts/tests/test_aide_lite.py` and `core/harness/tests/test_aide_lite.py`.
- `core/harness/*.py` maps with medium confidence to `core/harness/tests/test_<module>.py` and Harness smoke tests.
- `core/compat/*.py` maps with medium confidence to `core/compat/tests/test_<module>.py` and compatibility baseline tests.
- docs/config/script surfaces map with low confidence to structural Harness validation when no direct unit test exists.

## Determinism Notes

- Generated records use repo-relative paths only.
- Repo-map records are sorted by role and path.
- Snapshot records are sorted by path.
- Context index records source snapshot hash and generated artifact paths.
- Generated packets contain refs and metadata only, not raw source file contents.

## Limitations

- Role classification is path/extension heuristic only.
- Test-map confidence is heuristic only and may miss real test relationships.
- No embeddings, vector search, semantic search, or LLM file summaries are used.
- Exact line-ref validation exists, but excerpt extraction remains deferred.
