# Warning Dispositions

Accepted warning 1:

```text
RollbackBundle v0 remains proposed until acceptance.
```

Disposition: closed by this acceptance. RollbackBundle v0 is now accepted as `rollback_bundle_v0` only.

Accepted warning 2:

```text
Same-session independence is reduced, though no implementation repair was performed.
```

Disposition: accepted as warning-class because the independent check wrote only check-local queue/report/log artifacts and did not modify schema, helper, CLI, fixtures, tests, source reports, or downstream objects.

Accepted warning 3:

```text
Some reverse operation classes are represented and validated through fixtures rather than the live projection because the current accepted UpdatePlan source does not contain added managed file or added managed section operations.
```

Disposition: accepted as warning-class. Live projection coverage reflects the current accepted UpdatePlan. Fixture coverage proves the broader RollbackBundle operation vocabulary.
