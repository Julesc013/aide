# Remaining risks and gates

- A locally edited managed file still needs explicit resolution; this slice
  explains the conflict and preserves all payload bytes.
- Project-authored rationale is advisory and only bound to current file bytes.
  The author and historical intent cannot be inferred from a matching digest.
- Feedback packets include path and digest metadata plus any recorded rationale.
  They are local and should be reviewed by the project before manual sharing.
- The Windows privilege symlink case from prior combined qualification remains
  a skip, not a pass. Native and hosted qualification remain separate.
- Repair, rollback, and removal apply behavior are not delivered by this slice.
- No stable release, main promotion, tag, upload, or downloaded-asset result is
  claimed. The queue review gate applies to this new product source and the
  associated local packaging before dev integration.
