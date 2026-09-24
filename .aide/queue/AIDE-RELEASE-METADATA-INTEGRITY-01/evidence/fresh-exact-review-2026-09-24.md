# Exact release metadata review — 2026-09-24

Decision: **ACCEPT for `dev` integration only**.

Subject: `853d1c7a848621c52819f02a835db2a05f585641`, tree `b5f69ce15a8b9a14954151e500dd386cbfd62368`, base `cc85be9c472a16f39aae98ba00fd5de145098862`. This review was run from disposable checkout `D:\Projects\AIDE\_review_scratch\release-853d1c7a-newthread`. The candidate branch was not edited.

## Prior findings

- Missing paired JSON: closed. Deleting each source JSON in turn made `release bundle`, `validate`, `draft`, and `draft-validate` return 1. Both copied previews carried `blocked_stale_source_preview` and `publish_candidate: false`; both draft assets carried `blocked_stale` and `publish_candidate: false`. The checkout was restored and clean after each case. Source: `.aide/scripts/aide_lite.py:17322`; regressions: `test_q47_release_bundle.py:352`, `test_q48_github_release_draft.py:123`.
- Stale projection parent in commit prose: closed. `d6642c3d` has actual parent `7897f7de` and names that checkpoint in its message.
- Git replacement object defense: retained. The source sets `GIT_NO_REPLACE_OBJECTS=1` for ancestry and path comparisons; `test_export_import.py` includes a real replacement-object adversary and passed in this run.

## Verification

- Q31, export/import, Q47, Q48: 6 + 25 + 18 + 11 = 60 tests passed; no failures or skips. Logs: `review-test_q31_export_pack_governance.py.log`, `review-test_export_import.py.log`, `review-q47.log`, `review-test_q48_github_release_draft.py.log` in the disposable checkout.
- `release bundle`, `release validate`, `release draft`, `release draft-validate`: exit 0. All 44 tracked release files kept their SHA-256 bytes and the checkout stayed clean.
- The nine release asset-index paths matched actual SHA-256 and size. All seven checksum-index paths matched actual SHA-256.
- `doctor`, `validate`, and `pack-status`: exit 0; pack provenance `PASS_SOURCE_ANCESTOR`.
- `commit check --range 9f4bbc0a..HEAD`: five of five messages passed. `git diff --check origin/dev..HEAD`: passed. All 66 changed paths fit the task allowlist.

## Limits

This accepts local metadata integrity and source integration. It does not accept a complete stable product, hosted effects, main promotion, a tag, asset upload, or publication. The old Lovelace terminal output was not present in repository evidence and was not read from private Codex session storage.
