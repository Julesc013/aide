# CRLF pack template health repair, 2026-09-25

Independent delta review of frozen source `486aa2bd0f5f5255f216bd5f1654278574fe974b`, tree `739d46e6db715c9e11b55e8b6d116ff4a2ab8f95`, returned REQUEST_CHANGES. Actual report: `D:/Projects/AIDE/_review_scratch/repair-health-486aa2bd-independent-delta-review.md`, SHA-256 `30f0bde90756704a3d0e943235df293eaa23455cdcaba6cdd5106d14112d5de8`. It verified both earlier forged-receipt cases now fail closed, then reproduced a successful import from a checksum-valid CRLF `AGENTS.md.template` that health incorrectly called UNKNOWN. The inspector had used a helper that normalizes newlines when calculating the template block digest; import records the raw block digest. The reviewer preserved the exact script/log identities and target-before/after equality.

The new repair hashes the raw decoded pack managed block, exactly as import does, while retaining canonical mapping and receipt checks. A durable extracted-pack regression constructs a checksum-valid CRLF template, imports it into an authored CRLF target, then requires AGENTS MATCHING and overall HEALTHY with byte-identical target state before and after inspection.

Validation on the superseding uncommitted source in `D:/Projects/AIDE/aide-repair-health`, Windows Python 3:

- `py -3 -u -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k test_repair_health_accepts_raw_crlf_pack_agents_baseline -v`: exit 0, 1 test, 19.532 seconds. External log `D:/Projects/AIDE/_review_scratch/repair-health-crlf-pack-fix.log`, SHA-256 `1e21d42edf92ffeaa7dfa18c5bdb9dcec9d4e381f0fa031af5fb3ac91ff659d1`.
- `py -3 -u -B -m unittest discover -s .aide/scripts/tests -p test_export_import.py -k repair_health -v`: exit 0, 5 tests, 156.273 seconds. External log `D:/Projects/AIDE/_review_scratch/repair-health-focused-crlf-superseding.log`, SHA-256 `fe75b3d52307e9961b842988256944df448006a3221b0659fb34a6355ac610e8`.
- `git diff --check`: exit 0.

Source/test SHA-256 before freeze: `.aide/scripts/aide_lite.py` `163d8e38bb3ad1f2d8ca2c29c9a946b733b1246c5bf55dfac647b7b693796b57`; `.aide/scripts/tests/test_export_import.py` `bc95bdd57a36ae7dfaa8f2cf8cbff8e75e4cc76b9058ddf7c1ed3df200cbe353`.

This is a source-only repair. Independent exact rereview, combined tests, generated artifacts, post-commit replay and dev integration remain pending. The earlier REQUEST_CHANGES verdicts remain attached to their original frozen subjects.
