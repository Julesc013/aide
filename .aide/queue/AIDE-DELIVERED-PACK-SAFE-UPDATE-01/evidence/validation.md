# Validation

## Focused Results

- `py -3 -B -m py_compile .aide/scripts/aide_lite.py .aide/scripts/tests/test_export_import.py .aide/scripts/tests/test_q47_release_bundle.py`: PASS.
- Seven ownership, predecessor, conflict, stale-plan, and interruption tests: PASS (`7/7`).
- `py -3 -B .aide/scripts/tests/test_export_import.py -v`: PASS (`25/25`).
- `py -3 -B .aide/scripts/tests/test_q47_release_bundle.py -v`: PASS (`10/10`).
- Exact authored `AGENTS.md` byte preservation and idempotent rerun: PASS.

The Q47 consumer test executes the script stored inside extracted ZIP and
tar.gz artifacts with isolated Python, binds apply to the preview digest,
observes the target-local receipt, and verifies the second import is
`NO_CHANGES`.

## Adjacent Results

The adjacent suites passed 52 of 52 cases:

- Q31 export/import: `6/6`.
- self-consumer: `7/7`.
- distribution product status: `1/1`.
- DistributionApplyEngine: `9/9`.
- update plan: `7/7`.
- update receipt: `7/7`.
- rollback bundle: `7/7`.
- Q48 release draft: `8/8`.

## Repository And Artifact Results

- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py test`: PASS.
- `py -3 .aide/scripts/aide_lite.py pack-status`: PASS with
  `PASS_SOURCE_ANCESTOR`, valid checksums, and no boundary violations.
- `py -3 .aide/scripts/aide_lite.py release validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: PASS.
- `py -3 .aide/scripts/aide_lite.py commit check --range
  a2ba43624bf99d3354a2a7429a3241e3967310fc..HEAD`: PASS for all eight
  implementation and artifact commits before this evidence update.

The stabilized local release bundle is
`aide-lite-pack-v0-b1f97c5f30848128`, derived from clean implementation source
`31bd91bd10ed57e98e658380cd9372e074867f63`:

- ZIP: 973409 bytes,
  `9bc5078fc7673e51fda10568bb2bc575d44c07de4889922178d7980819f8ff2b`.
- tar.gz: 645708 bytes,
  `23f6cb2cf5ba59866aceddd91f2b556da8c8686bdf40d86c631c016d0bde81fb`.

An external predecessor canary installed the prior published ZIP, then used
the new extracted CLI with a separately validated predecessor pack. Preview,
exact-plan apply, receipt observation, and no-op rerun passed. A subsequent
managed-file edit produced `CONFLICT` without changing an unrelated guard
file. Authored bytes outside the `AGENTS.md` managed section remained exact.

The release records remain `preview_only` and `no_publish`. No tag, upload,
GitHub Release, network API, main mutation, or non-disposable target mutation
occurred.
