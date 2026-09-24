# Qualified local candidate

**Superseded after qualification:** the dry-run pending-intent recovery finding
was outside this candidate's test matrix. These recorded results remain true for
the identified bytes, but this is not the current review subject.

Date: 2026-09-24 AEST. Source checkpoint `98de5ee1531e3d71f6f003f8bc98bf2a6b8bf23b`;
preview checkpoint `9dc91654f8df9d7ea8b85dc32285b504f3344e26`;
artifact checkpoint `8262b2fd64658cdb6ee8638fc4aad6221ecfee94`;
source-ancestor projection candidate `37daa862e939ec4b4b299474e26668a6e44c54e2`
with tree `118e3771fd9ce82cf43425bbabbf3677244fcddb`.

| Check | Result |
|---|---|
| Export/import suite | 27/27 PASS; two affected cases reran PASS after final digest-field edit |
| Q47 local release bundle | 18/18 PASS |
| Q48 local GitHub release draft | 11/11 PASS |
| Q31 export governance | 6/6 PASS |
| Changelog preview/validate/status | PASS; 50 commits, zero malformed; preview only |
| Export boundary and pack-status | 826 files, 829 checksum entries; `PASS_SOURCE_ANCESTOR`; zero problems |
| Local release validate and draft-validate | PASS; no tag, upload, or publication |
| Asset integrity | 9 assets and 7 checksum records, zero mismatches |
| Generator replay | before artifact commit: 44/0 changed; first post-commit: 18 expected projection changes; second: 44/0; committed projection clean-tree: 44/0 |
| Canonical `validate` and `doctor` | Exit zero, logs in external review scratch |
| `git diff --check` | PASS |

Final local archive hashes: ZIP
`1b972fb1c96b1d673620e3543f079e10da13ec4fac1473379b8528294de25052`;
tar.gz `9b0a5bd0943d160dbd16059276c47a89aa573777de5df6ba5c2d19093757650f`.
The ZIP contained the current `aide_lite.py`; it was extracted and executed
with isolated Python in a disposable Git target. The prior dev ZIP was also
extracted and applied first. The old-to-new update stopped on a direct-edit
conflict, preserved project-owned profile and manual guidance, and generated
known digest-bound rationale only on explicit local feedback request. Original
receipt: `D:\Projects\AIDE\_review_scratch\customization-consumer-cc34021a8351\receipt.json`.
Copied `extracted-consumer-receipt.json` is byte-identical; SHA-256
`a1be1f77db1a54db3c6662cfd8c557d55c0b1d6783e2dbed4b5582d7aaa60bce`.
The current ZIP is unchanged after projection replay.

Logs: `D:\Projects\AIDE\_review_scratch\customization-q47-tests.log`,
`customization-q48-tests.log`, `customization-q31-tests.log`,
`customization-validate.log`, `customization-doctor.log`, and
`combined-customization-*.log`. These are recorded command results, not
hosted qualification or published-asset acquisition.
