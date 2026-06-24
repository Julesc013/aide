# Validation Results

Initial results:

- Focused compile and unit tests passed.
- Shared provider regression tests passed.
- Existing AIDE self-validation adapter tests passed.
- Existing Dominium registered-validation adapter tests passed.
- The single live Eureka invocation passed with warnings.
- Adapter report validation passed with warnings and `missing_evidence: 0`.
- Queue task inspection passed with classification `complete`.
- Queue task evidence inspection passed with no missing evidence.
- Broad `aide_lite.py validate` passed.
- New-surface local path and secret-like scans passed.
- `git diff --check` passed.
- `git diff --cached --check` passed after staging.

Commit policy is performed after commit.
