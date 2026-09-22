# Validation

- `py -3 -B .aide/scripts/tests/test_q27_commit_recovery.py -v`: PASS, 19 tests.
- `py -3 -B -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_q27_commit_recovery.py`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py doctor`: PASS.
- `py -3 -B .aide/scripts/aide_lite.py eval run --task commit_message_standard_golden`: PASS, 22/22 checks; generated latest-run reports were restored because they are outside task scope.
- Raw range checks for `bfb86c12^!`, `486e81cd^!`, and `1011d008^!`:
  FAIL with the exact retained failures recorded in `raw-policy-failures.md`.
- Default range checks for all three proposed records: FAIL with
  `disposition_status: proposed` and `disposition is proposed and has no effect`.
- `py -3 -B .aide/scripts/aide_lite.py pack-status`: PASS for the predecessor pack; a clean-source refresh is still required to carry the new portable policy, schema, helper, and docs.
- `git diff --check`: PASS for the current source change.

## Final Candidate

- Clean portable source commit: `0dc74af4fea257f8c56ae0848e43215288ed9edf`.
- Clean portable source tree: `41137c8be01cecf200049a876d94f0d18ebc0a8e`.
- Generated pack commit: `f409dba82e5324a2f9605f6f4c4efcceee3a5318`.
- Manifest SHA-256: `34d7e364f7f21158d33e8bdb0ddf4bcf5decb5410ef3d6a349b0d86568f0935c`.
- Checksums SHA-256: `264b0a327223afb73fd935edb78a4330e3b2418743cdaeabff4db45d52b9f501`.
- `py -3 -B .aide/scripts/tests/test_q31_export_pack_governance.py -v`: PASS, 6 tests in 43.475 seconds.
- `py -3 -B .aide/scripts/tests/test_export_import.py -v`: PASS, 25 tests in 271.747 seconds.
- Refreshed `pack-status`: PASS; checksum problems 0, provenance `PASS_SOURCE_ANCESTOR`, boundary violations 0.
- Portable payload presence: general policy, schema, helper, tests, and docs present; source-specific registry absent.
- `release validate`: PASS against retained local no-publish artifacts.
- `release draft-validate`: PASS; tag, upload, GitHub Release, network, branch mutation, and active CI all remain false.
- `commit check --range c6fdc754844cf7d42302218ce08307a7e05dcb61..HEAD --no-dispositions`: PASS, 4 commits.
- Final canonical `validate` exit: 0.
- Final canonical `doctor` exit: 0.

The earlier predecessor-pack line above is retained as execution history; the
final refreshed result supersedes its stated refresh requirement.
