# Validation Results

See `validation.md` for detailed command outcomes.

## Summary

- Overall validation status: `PASS_WITH_WARNINGS`
- Blocking failures: none
- Non-blocking warnings:
  - `.aide/queue/index.yaml` CRLF normalization warning.
  - Pre-check latest commit message did not follow AIDE commit policy, but that commit is unrelated to the checked charter; the checked charter commit passed direct commit-message validation, and this check commit passed post-commit validation.

## Key Passes

- Broad `doctor`: PASS after latest-task packet section repair.
- Broad `validate`: PASS after latest-task packet section repair.
- Build task inspect/evidence: PASS.
- Check task findings JSON parse: PASS.
- Markdown/JSON finding agreement: PASS.
- JSON report parsing: PASS.
- Repo-local simple YAML parsing: PASS.
- Post-commit latest commit check: PASS.
