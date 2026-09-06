Promote the already integrated ULK workspace-hygiene unit to canonical main before admitting the next completed provider unit. This preserves the repository’s limit of one completed, unpromoted WorkUnit.

Source: `dev@0e8bcc38f5a55c80974c41da8d2eac10ac703593`; tree: `b28499daea1088504708691e794dbbbd59998f18`. Current main: `5479939ca5cbc9ee0f901608a92012778b4752ae`.

The change provides marker-owned external development storage and bounded worktree cleanup. Review the existing workspace-hygiene checkpoint and current GitHub Checks on this promotion candidate. No runtime/public ABI/package version change, tag, publication or FacMan consumer repin is included.

The separately reviewed PR #18 correction is committed and green at `151a18f9f67af1a1ede17bda72641155d22106e5`; it will integrate after this promotion and required ancestry synchronization.

Work-Item: UNIVERSAL-LAUNCHER-WORKSPACE-HYGIENE-01
