# Historical Failure Review

The original failed check remains a preserved `FAILED_VALIDATION` record.

The acceptance retains the failure chain:

- original result: `FAILED_VALIDATION`;
- repair result: `PASS_WITH_WARNINGS`;
- repair-check result: `PASS_WITH_WARNINGS`.

The original material defects are not erased:

- list fixtures emitted `null` optional cursor fields;
- `resource-not-found-refusal.json` used `-32043` instead of `-32002`.
