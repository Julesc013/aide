# Authored AGENTS backup review repair

Date: 2026-09-25. Source-only task worktree: `D:/Projects/AIDE/aide-removal-combined`.

## Review subject and finding

- Rejected source commit: `d5b44626d6f9efc6f90c8b8eda1e990e5864b5af`, tree `5754734fd59ad66744b3b5b265f06218d26ebdb6`.
- Independent review original: `D:/Projects/AIDE/_review_scratch/removal-section-d5b44626-independent-review.md`, SHA-256 `38876eb382b6e8115599365d0b8703ae8782fafdb3d79b419b310a0138e3392a`. Decision: REQUEST_CHANGES. Do not attribute acceptance to this report.
- RED reproduction: exact original backup and altered backup each survived a retry that incorrectly returned `DETACHED`; the new two-case regression failed on both before the repair.

## Repair and evidence

The removal intent now records the original AGENTS Windows volume and file identity along with the exact preimage digest. Recovery observations classify any deterministic backup as unresolved. The terminal path holds the verified AGENTS postimage handle while an anchored, single-link, no-reparse backup handle checks both original digest and file identity before disposition. An absent AGENTS target with backup, an altered or same-byte substituted backup, and an interrupted rename-before-link retain receipt and intent as `RECOVERY_REQUIRED`. A source-only legacy intent lacking original identity cannot auto-clean a backup.

- `.aide/scripts/aide_lite.py` SHA-256 `182e0acb699fdc29000f07e2e9ee337b3c319922d4d093e5884432ff8f189694`.
- `.aide/scripts/tests/test_export_import.py` SHA-256 `dd33369bb4b61703dd8e262430b42446064f11a9177eac8ea4774434bbb13ff5`.
- `py -3 -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k brownfield_section`: exit 0; 8 tests, 247.733 s, OK. Log `D:/Projects/AIDE/_review_scratch/removal-section-backup-repair-focused.log`, SHA-256 `064ca83e04adbcc12025b90fd413b661c9a498d080a81745f1c1029696103d3e`.
- `py -3 -B .aide/scripts/aide_lite.py validate`: exit 1 solely due to existing export-pack manifest source commit `49318d50472b17f648c2f29e998239b9c446cf14` not matching source-only worktree HEAD `d5b44626d6f9efc6f90c8b8eda1e990e5864b5af`. The two failure lines are export pack provenance and pack-status. Log `D:/Projects/AIDE/_review_scratch/removal-section-backup-repair-validate.log`, SHA-256 `882363d9bf351a689a233eb8ebbcde64e8b6df91940acf439cf09f4166d49f50`.
- `git diff --check`: exit 0.

No generated pack or release artifact was rebuilt. This repair needs independent exact-source rereview, then combined-source artifact regeneration, validation, disposable consumers, and an integration decision. The receipt remains the recovery authority for unresolved backup states.
