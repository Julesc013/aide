# Workspace Containment

The repair stages the reference worker into a disposable temporary workspace and invokes the staged worker with the provider working directory set to that workspace.

The source checkout is not used as the worker cwd. The report records:

- `workspace_ref: aide://workspace/local-process/reference-01`
- `workspace_root_inside_source: false`
- `workspace_cleanup.removed: true`

The resolver rejects:

- absolute members;
- `.` and `..` traversal;
- lexical path escapes;
- symlink components;
- Windows reparse-point components when visible through `st_file_attributes`.

Focused unit coverage exercises traversal, absolute path, symlink escape, and inside-source workspace refusal.
