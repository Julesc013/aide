# Workspace Containment Review

- REQUEST_CHANGES: live process cwd is recorded as `<aide-root>`, not a disposable worker workspace.
- REQUEST_CHANGES: source code does not prove path traversal, symlink, or reparse-point escape rejection.
- Source checkout remained unchanged within declared probe coverage, but that is weaker than workspace containment.
