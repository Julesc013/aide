# Validation

## Admission Checkpoint

| Command | Result |
|---|---|
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 352 source queue tasks and WorkUnit objects validated |
| `py -3 -B .aide/scripts/aide_lite.py validate` | PASS |
| `git diff --check` | PASS |
| Staged path inspection | PASS; 89 exact files, zero forbidden prefixes |
| `git ls-remote --heads origin main dev task/aide-cw-integration-broker-01` | PASS; remote refs matched the recorded source and target heads |

The candidate-specific and post-integration checks remain pending. Refreshed
validator report snapshots were not retained because this task does not own
those generated paths.

## Documentation Candidate

| Command or check | Result |
|---|---|
| `tools/verify_import.py --test-patch` | PASS; 30 captured blobs, 29 preserved files, six adopted contracts, 34 drafts, 244 requirement aliases, 244 unrun acceptance designs, 119 package links, exact patch round trip |
| `python -m unittest discover -s tools/tests -v` | PASS; 13 passed, one Windows symlink-capability test skipped |
| `tools/check_import.py --repo <candidate>` | REFUSED as expected/inapplicable after materialization; it detected the changed base and existing destination paths and performed zero writes |
| Manifest destination SHA-256 comparison | PASS; 40 checked, zero mismatches |
| Adopted-contract SHA-256 comparison | PASS; all six match the recorded import manifest |
| Draft frontmatter count | PASS; 34 files have `status: draft` |
| Alias scan | PASS; 244 unique `UR-*` and 244 unique `UC-*` aliases |
| Acceptance execution field | PASS; manifest remains `behavioral_cases_executed: 0` |
| Relative Markdown link scan | PASS; 127 checked, zero missing |
| Source blob comparison | PASS; 45 specification/navigation paths match source checkpoint `9a1da8b8` exactly |
| `py -3 -B .aide/scripts/aide_lite.py workunit validate` | PASS; 349 source queue tasks and objects validated |
| `py -3 -B .aide/scripts/aide_lite.py validate` | PASS |
| `git diff --check` | PASS |

No broker, isolated-host, or behavioral acceptance suite was run for this
documentation candidate. The package's one skipped symlink fixture remains a
skip, not a pass. Generated validator report refreshes were restored because
this WorkUnit does not own those paths.
