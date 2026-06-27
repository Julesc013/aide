# Independent Probe Summary

The check-local probe loaded `core/protocol/update_plan.py`, the committed schema, the generated projection, the generated validation report, and the generated fixture matrix.

Probe result:

```text
PASS
```

Coverage:

- Schema operation classes: all 15 required classes.
- Helper operation classes: all 15 required classes.
- Positive operation-class probes: `15`.
- Fail-closed probes: `23`.
- Fixture cases checked: `29`.
- Validation report errors: `0`.

Live projected operation classes:

- `manual_review_required`
- `preserve_evidence_only`
- `preserve_legacy`
- `preserve_local_only`
- `preserve_project_overlay`
- `preserve_project_owned`
- `preserve_runtime_generated`
- `refuse`
- `regenerate_project_output`
- `update_managed_file`
- `update_managed_section`

Not every possible operation class appears in the single live projection. This is not material because the schema and helper support all required classes, the validator accepts each class in a valid context, and the required fixture matrix passes. The concrete projection only describes the current dry-run plan.

Projected conflicts:

- `never_touch_refusal` at `.git/**`, disposition `fail_closed_no_apply`.
- `manual_review_required` at `unclassified/**`, disposition `fail_closed_no_apply`.

The unknown ownership case is warning-class because the planned operation is `manual_review_required`, the ownership class is `unknown`, and no update apply or target mutation authority is claimed.
