# Q37 Repo Intelligence Report

## Summary

Q37 adds deterministic, repo-local, no-call repo intelligence indexing. It reads
git-tracked files when Git is available, falls back to a bounded filesystem walk
when needed, excludes `.git` and `.aide.local/`, computes sizes and SHA-256
hashes, classifies files, and writes JSON/Markdown outputs under `.aide/repo/`.

## Generated Outputs

- `.aide/repo/file-inventory.json`
- `.aide/repo/ownership-map.json`
- `.aide/repo/dependency-map.json`
- `.aide/repo/test-map.json`
- `.aide/repo/doc-link-map.json`
- `.aide/repo/generated-map.json`
- `.aide/repo/orphan-candidates.json`
- `.aide/repo/latest-repo-intelligence.md`

## Latest Counts

- source_commit: `c9f77de4d4f02527813cb285e0d6ea0e8868286c`
- source_mode: `git_tracked_files`
- file_count: 1,543
- unknown_count: 146
- generated_count: 324
- evidence_count: 500
- orphan_candidate_count: 451

## Counts By Kind

- contract: 10
- doc: 313
- evidence: 500
- fixture: 109
- generated: 324
- policy: 43
- schema: 9
- source: 37
- template: 11
- test: 35
- tool: 6
- unknown: 146

## Warnings

- Unknown classifications are preserved for follow-up instead of being hidden.
- Orphan candidates are conservative inspection candidates, not deletion advice.
- Stale doc-link candidates are broad heuristic findings and need Q38/Q39 review.

## Safety

- provider_or_model_calls: none
- network_calls: none
- file_moves: false
- file_deletes: false
- target_repo_mutation: false
