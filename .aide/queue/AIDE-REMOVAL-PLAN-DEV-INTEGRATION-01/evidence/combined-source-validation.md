# Combined removal-planner source validation

Candidate before merge commit: HEAD `7bc4c9b5087bfdb09b06c6b6cb62ff0707e98878`,
MERGE_HEAD `d1362f912c951ccc6022d0a2a3a527a4d66365f1`. The staged tree
before this evidence edit was `d57e524444ac7a555be6f87e1ff7811d6bcfbee0`.
Current-dev generated export, release, changelog, and intake files were not
staged from the old branch. The 6 changelog previews rewritten by tests were
restored to HEAD after those tests.

| Check | Result | External log SHA-256 |
|---|---|---|
| `test_export_import.py -v` | PASS, 32 tests, 498.477s | `8f750b74faabe8637eb215ad96eca58a10c274bb844592da8adfe5f22d8d6671` |
| `test_q47_release_bundle.py -v` | PASS, 18 tests | `7f0ff2360245fafe237841d2f3de850bb98a9c2a668aa50f6d708419bf962c17` |
| `test_q48_github_release_draft.py -v` | PASS, 11 tests | `24d6b9f574bda4387eb077ddad9ad62d549ebd6024d0ddc898eaf480d29c1b28` |
| `test_q34_changelog_release.py -v` | PASS, 11 tests | `e583937d472882f54820123a2356510f98ca61f406d53e7822d830f344af9536` |
| `test_q31_export_pack_governance.py -v` | PASS, 6 tests | `e5b4d269273e7b0bd04a43ca984e3b5579aad9dd2c66c9d1abd88bd3b50ab29f` |
| `aide_lite.py validate` | PASS | `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faee83b383e789` |
| `aide_lite.py doctor` | PASS | `e4e2deaa87a66ea30d9ed805badb0b9fca39228a828799032149970a68d318fb` |
| `commit check --range c6fdc754..d1362f91` | PASS_WITH_DISPOSITIONS for exact owner B | `36422899da44fee1798db6739a02519cbbb8007f3cf2ed7bc9601dd6f79d9d02` |
| Same range `--no-dispositions` | Expected FAIL, 13 raw B formatting defects | `16d643eeacb5d723569d3c811d20cc7837b6a28959e387c71f3f015beffb9e90` |

`py_compile` of the combined CLI and two affected suites, `git diff --cached
--check`, and conflict-marker and unmerged-path scans passed. These are
combined-source results before the new pack is generated. They do not qualify
the final integrated archive, deletion, native effects, hosted effects, or a
stable release.
