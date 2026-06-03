# AIDE-APPLY-02 Validation Checklist

## Required Authorization Validation

- `git status --short --branch`
- `git remote -v`
- `git rev-parse HEAD`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- boundary text searches over this queue packet
- local secret scan over changed files

## Required Future Implementation Validation

- `git status --short --branch`
- `git diff --check`
- `py -3 .aide/scripts/aide_lite.py task status`
- `py -3 .aide/scripts/aide_lite.py managed-section status`
- `py -3 .aide/scripts/aide_lite.py managed-section validate`
- `py -3 .aide/scripts/aide_lite.py managed-section fixture-verify`
- `py -3 .aide/scripts/aide_lite.py transaction status`
- `py -3 .aide/scripts/aide_lite.py transaction validate`
- `py -3 .aide/scripts/aide_lite.py transaction fixture-verify`
- targeted executor unit tests
- fixture tests for allowed managed-section replacement and blocked conflict cases
- capability reality checks or reports if capability labels are changed
- export-pack and manifest checks if export or generated manifest paths are changed
- review/evidence packet generation where supported
- boundary text searches
- local secret scan over changed files

## Required Future Test Cases

- dry-run produces no file mutation;
- allowed managed-section replacement succeeds in fixture;
- disallowed path is blocked;
- protected path is blocked;
- path traversal is blocked;
- unsupported operation is blocked;
- missing operation is blocked;
- missing marker is blocked;
- duplicate marker is blocked;
- malformed marker is blocked;
- nested marker is blocked;
- ambiguous marker ownership is blocked;
- preimage hash mismatch is blocked;
- postimage mismatch is detected;
- rollback-compatible record is generated;
- staged-change record is generated;
- manual content outside markers is preserved;
- report/evidence output is generated;
- capability label is not overstated.

Generated report refreshes outside the task allowlist must be restored or explicitly classified before concluding.
