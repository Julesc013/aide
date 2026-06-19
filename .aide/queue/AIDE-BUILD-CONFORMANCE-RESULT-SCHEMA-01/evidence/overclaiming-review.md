# Overclaiming Review

The generated reports and CLI preserve these false/null boundaries:

- `execution_performed: false`
- `runner_ref: null`
- `admission_performed: false`
- `subject_admitted: false`
- `trusted: false`
- runtime false
- mutating false
- provider/model calls none
- network calls false
- Gateway calls none

The result may satisfy profile requirements by evidence projection, but it does
not admit the subject, grant trust, activate the profile, execute a capability,
or implement runtime behavior.
