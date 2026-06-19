# Root Cause Analysis

The drive-prefix defect came from `_is_absolute_repo_path` only rejecting Windows
drive strings when the colon was followed by `/` or `\\`. Windows drive-relative
strings such as `C:repo/file.txt` therefore passed as repository-relative
locators.

The duplicate-normalization defect came from collecting normalized paths without
checking whether two original path strings collapsed to the same normalized
locator.

The repair adds:

- leading Windows drive-prefix rejection for any `^[A-Za-z]:` path string;
- duplicate normalized path detection for allowed, forbidden, and declared path
  lists.

No schema, projection identity, apply behavior, approval behavior, or trust
behavior was changed.
