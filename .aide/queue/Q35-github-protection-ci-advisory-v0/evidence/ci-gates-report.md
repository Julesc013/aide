# CI Gates Report

Q35 defines advisory CI gates only. It does not create or install workflow
files.

Recommended future gates:

- Harness validate, doctor, and self-check.
- AIDE Lite validate, test, selftest, and eval.
- Commit check and changelog validation.
- Git policy and GitHub advisory validation.
- Pack status and targeted secret scan.

Future CI activation requires a separate reviewed apply phase with rollback and
operator approval.
