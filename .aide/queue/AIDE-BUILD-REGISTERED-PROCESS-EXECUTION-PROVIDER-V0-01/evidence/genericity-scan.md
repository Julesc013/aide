# Genericity Scan

Command:

```text
rg -n "dominium|Dominium|AIDE-BUILD|AIDE-CHECK|registered-validation|validation.run" core\execution core\protocol\process_invocation.py core\protocol\execution_receipt.py
```

Result:

```text
PASS: no matches
```

The generic provider and protocol files contain no Dominium task IDs,
capability IDs, report paths, refusal codes, source paths, repository URLs,
machine-specific absolute paths, or domain-specific branches.
