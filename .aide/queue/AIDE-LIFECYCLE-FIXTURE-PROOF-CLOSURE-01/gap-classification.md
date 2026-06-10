# Expected-Report Gap Classification

## Result

`REPAIR_BEFORE_FIXTURE_APPLY_GATE`

## Missing Static Expected Report Refs

| Scenario | Area | Prior classification | Closure classification |
| --- | --- | --- | --- |
| `install-clean` | install | non-blocking for install checkpoint | repair before fixture apply gate |
| `install-existing-manual-preserved` | install | non-blocking for install checkpoint | repair before fixture apply gate |
| `upgrade-manual-preserved` | upgrade | non-blocking for upgrade checkpoint | repair before fixture apply gate |
| `repair-plan-missing-marker` | repair | non-blocking for repair checkpoint | repair before fixture apply gate |
| `repair-plan-malformed-marker` | repair | non-blocking for repair checkpoint | repair before fixture apply gate |
| `uninstall-manual-preserved` | uninstall | non-blocking for uninstall checkpoint | repair before fixture apply gate |

## Rationale

The generated plan reports and expected-state fallback evidence were sufficient for dry-run checkpointing. They are not as strong as static expected report refs for the first fixture apply gate, where expected-vs-actual comparison should be deterministic and reviewable without regenerating source truth.
