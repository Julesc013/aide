# Path Classification

The repair adds deterministic lexical path classification before host path
resolution.

Covered refusal classes:

- `workspace_path_absolute`
- `workspace_path_traversal`
- `workspace_path_escape`
- `workspace_symlink_escape`
- `workspace_reparse_point_escape`
- `artifact_path_escape`
- `artifact_link_rejected`

Focused tests cover:

- safe nested regular file;
- safe nested artifact directory;
- nested traversal;
- POSIX absolute path;
- Windows drive absolute paths with slash and backslash;
- UNC path;
- rooted Windows path;
- final-member symlink;
- intermediate symlink;
- artifact absolute/traversal path.

Reparse-point practical fixtures remain platform-dependent. The implementation
checks file attributes with `follow_symlinks=False` when such paths exist.
