# Remaining Risks

- The provider remains proposed and unaccepted.
- Independent repair check is required before provider reuse proof resumes.
- Process cancellation is declared unsupported in v0 rather than implemented.
- Full child-process-tree termination is not implemented.
- Persistent idempotency, resource quotas, streaming artifact storage, and
  non-Git state providers remain future work.
- The repair relies on focused fake-runner and fixture parity tests; the live
  Dominium command was not rerun.
