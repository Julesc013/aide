# Static Review

## Material Findings

### Required example plan is not a passing runnable plan

The checked-in example `.aide/examples/apply/scoped-transaction-executor.dry-run.example.json` uses placeholder hashes:

- `expected_preimage_hash: sha256:example-preimage`
- `expected_postimage_hash: sha256:example-postimage`

The required run command fails closed with `BLOCKED_PREIMAGE_HASH_MISMATCH`. No target mutation occurred. Repair should make the example runnable with fixture-current hashes or split the documentation-only example from a checked validation plan.

### Resolved target path safety is incomplete

`core/apply/transaction_executor.py` rejects absolute paths, traversal, wildcard characters, protected paths, and paths outside lexical allowed roots. It does not resolve the final target path and prove that it remains under the repo root and allowed roots after symlink or Windows reparse-point resolution before reading or writing.

Repair should add resolved target validation before file read and write, reject symlink/reparse-point escape, and add tests where platform support permits.

### Apply mode has partial mutation risk after late failure

`apply_staged_changes` writes staged changes sequentially. Earlier writes can remain if a later write/read or postimage verification fails. The failure is reported, but v0 does not yet provide atomic staging, a one-target apply limit, or automatic restore behavior.

Repair should either constrain apply mode to one target for v0 or add stronger staging/rollback-compatible handling with tests for multi-operation failure.

### Direct core report output omits self `report_path`

`write_available_outputs` writes the report file before setting `report["report_path"]`. Direct core execution can persist a final report that does not include its own report path, even though the returned object and AIDE Lite fixture wrapper can include it.

Repair should assign `report_path` before writing the report and add a direct core-output test.

## Covered Areas

- path normalization rejects absolute paths, traversal, wildcard characters, protected paths, and paths outside allowed roots.
- operation allowlist rejects missing, ambiguous, unsupported, and forbidden operation types.
- managed-section integration delegates marker parsing to `core.apply.managed_sections`.
- missing, duplicate, malformed, nested, and ambiguous marker cases are tested.
- preimage hash mismatches block mutation.
- planned postimage mismatches are detected.
- apply mode is explicit and verifies post-write content.
- dry-run/report modes do not mutate target files in tests and fixture commands.
- staged-change and rollback-compatible records are generated.
- report schema and plan schema parse as JSON.
- tests use temporary directories or repo-approved fixture/report paths.

## Non-Blocking Notes

- `scoped-transaction run --plan` resolves relative plan paths against the shell working directory, not `--repo-root`.
- The report schema remains permissive with `additionalProperties: true`; this is acceptable for v0 but should be revisited before broader apply surfaces.
