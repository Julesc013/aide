# Validation

## Candidate

- Initial base: `dev@13fc9a6a0aa02bd4c2343c640e8b83a95d89c6ab`.
- Synchronized base: `dev@c6fdc754844cf7d42302218ce08307a7e05dcb61`.
- Qualified source: `dd26c9fc67eee9d5da4b1484d9fabccf3c2e21ab`.
- Artifact materialization: `a551cd072a915b17ff4db191ce3c2437d99f70fe`.
- Provenance closure: `3306315bd6d0024f4c017ec419f95d9399de6edb`.
- Qualified source tree: `00378b4c4978d3053981d7db46f46d5f8997f921`.

## Commands And Results

- `py -3 -B -m py_compile ...`: PASS.
- Three focused removal-plan tests: PASS in 53.137 seconds.
- `test_export_import.py -v`: PASS, 28 tests in 312.180 seconds.
- `test_q47_release_bundle.py -v`: PASS, 10 tests in 21.512 seconds.
- `aide_lite.py pack-status`: PASS with `PASS_SOURCE_ANCESTOR` provenance.
- `aide_lite.py release validate`: PASS.
- `aide_lite.py release draft-validate`: PASS.
- `aide_lite.py validate`: PASS.
- `aide_lite.py doctor`: PASS.
- `aide_lite.py intent validate`: PASS.
- JSON parsing, conflict-marker scan, and `git diff --check`: PASS.
- Exact extracted ZIP consumer import and `plan-removal --json`: PASS.
- Exact extracted tar.gz consumer import and `plan-removal --json`: PASS.
- Target-tree digest before and after each plan: unchanged.
- Provider/model/network calls: none.
- Target writes by removal planning: none.
- Tags, uploads, publication, and main mutation: none.

## Commit Conformance

- Latest merge, artifact, and provenance commits: PASS.
- Published implementation commit
  `486e81cd3a918729f28e4b452a9dcff017238a04`: FAIL because its detailed body
  omitted required bullets, category prefix, and trailers.
- The failure is retained exactly; history was not rewritten and strict checks
  were not weakened. Dev integration awaits the separately scoped exact
  historical disposition.
