# Path Safety Review

Implemented and passing:

- POSIX absolute path refusal.
- Windows drive path refusal.
- UNC-style absolute path refusal through normalization.
- Traversal path refusal.
- `latest-` source-state contamination refusal.

Material gap: path safety is not paired with path collision, case-fold collision,
symlink/reparse classification, or section identity collision checks.
