# Q12 Verification Fixtures

## Fixture Strategy

Q12 uses tempfile-created fixtures in tests rather than committed secret-like fixture files. This avoids storing fake provider-key-shaped values in the repo while still exercising secret-scan logic.

## Covered Cases

- Valid evidence packet required sections.
- Missing evidence packet section failure.
- Valid task packet section checks.
- Task packet forbidden prompt-pattern warning.
- Conservative file-reference extraction from backticks and markdown-style refs.
- Existing file reference pass.
- Missing file reference warning.
- Valid `path#Lstart-Lend` line range.
- Invalid line range failure.
- Secret-like assignment detection with runtime-constructed fake values.
- Policy-text false positive allowance for terms like `api_key`.
- Diff-scope classification for allowed, forbidden, unknown, and deleted paths.
- Adapter managed-section drift detection.
- Verification result values: PASS, WARN, FAIL.
- Verification command failure for missing evidence packet.
- Verification report rendering without raw source markers.
- Bounded write-report path enforcement.
- Selftest verifier coverage.

## Test Files

- `.aide/scripts/tests/test_verifier.py`
- `.aide/scripts/tests/test_aide_lite.py`
- `core/harness/tests/test_aide_verifier.py`

## Known Limits

- Fixtures are structural and deterministic; they do not simulate full semantic diffs or real provider secrets.
- Direct unittest discovery with `-s .aide/scripts/tests -t .` remains blocked by Python hidden-directory importability; direct discovery without `-t .` and Harness mirror tests pass.
