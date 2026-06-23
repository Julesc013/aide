# Source Chain

The acceptance source chain is:

```text
AIDE-BUILD-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
-> AIDE-CHECK-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
-> AIDE-ACCEPT-DOMINIUM-WORKUNIT-VALIDATION-SLICE-01
```

Build:

- result: `PASS_WITH_WARNINGS`
- missing_evidence: `0`
- warning: fixture-backed local callable, not a general Dominium command runner

Check:

- result: `PASS_WITH_WARNINGS`
- material_finding_count: `0`
- missing_evidence: `0`
- accepted capability label: `fixture_backed_dominium_validation_adapter`
- live Dominium command execution proven: `false`

Acceptance therefore accepts only `fixture_backed_dominium_validation_adapter`.
