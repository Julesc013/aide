# Secret Scan

## Result

PASS with documented raw-scan false positives.

## Commands

Raw marker scan:

```text
rg -n -i "SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_ACCESS_KEY|AWS_SECRET_ACCESS_KEY" .aide/queue/AIDE-CHECK-APPLY-02 .aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0 core/apply/transaction_executor.py core/apply/tests/test_transaction_executor.py .aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py .aide/policies/scoped-transaction-executor.yaml .aide/apply/scoped-transaction-executor.schema.json .aide/apply/transaction-executor-report.schema.json .aide/examples/apply/scoped-transaction-executor.dry-run.example.json docs/reference/scoped-transaction-executor.md
```

Result: WARN false positives only. Matches were protected-path text such as `secrets/**`, references to secret scan evidence, and the scan pattern itself.

Refined credential-shaped scan:

```text
rg -n -i "-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[0-9A-Za-z_-]{20,}|(OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID|GITHUB_TOKEN|PASSWORD|API_KEY|TOKEN|SECRET)\s*[:=]\s*['\"][^'\"]{8,}" .aide/queue/AIDE-CHECK-APPLY-02 .aide/queue/AIDE-APPLY-02-scoped-transaction-executor-v0 core/apply/transaction_executor.py core/apply/tests/test_transaction_executor.py .aide/scripts/tests/test_aide_apply_02_scoped_transaction_executor.py .aide/policies/scoped-transaction-executor.yaml .aide/apply/scoped-transaction-executor.schema.json .aide/apply/transaction-executor-report.schema.json .aide/examples/apply/scoped-transaction-executor.dry-run.example.json docs/reference/scoped-transaction-executor.md
```

Result: PASS; no credential-shaped secrets found.

Network tools, GitHub, providers, and Gateway were not used.
