# Warning Disposition

The acceptance blocker is not ordinary warning debt. It is a material failed
validation result from the independent check.

Blocking findings:

- `path_scope_drive_prefixed_relative_accepted`
- `path_scope_duplicate_normalization_accepted`

Deferred capability warnings remain true but are not the reason this task is
blocked:

- no general diff parser;
- no artifact resolver;
- no VCS reachability verification;
- no policy engine;
- no approval engine;
- no apply engine;
- no rollback execution;
- no conformance runner;
- no admission or trust;
- no runtime.
