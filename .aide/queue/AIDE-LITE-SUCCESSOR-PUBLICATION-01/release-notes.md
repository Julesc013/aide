**AIDE Lite 1.1.0** adds task continuation views, Git policy inspection,
review and reuse reports, and work-effort summaries to the local CLI. It also
fixes effort reporting in adopted projects so it uses AIDE's installed helper.

- **Added:** the 18 command forms listed in the attached manifest, including
  `task current`, `task resume-plan`, `git policy`, `review-pack`, `quality reuse`
  and `job effort`. The 38 previously declared forms remain in the contract.
- **Upgrade:** tested from the actual published 1.0.0 package with project
  customization, direct edits, upstream conflicts, recorded resolutions,
  interrupted imports and recovery. Inspect the dry-run plan before applying;
  preserve the original packs and project state for recovery.
- **Qualified profile:** T3 companion local Windows CLI, tested on Windows 10
  build 19045 with Python 3.14.8. The manifest lists all 56 qualified forms.
  Other command forms, hosts and environments have no new support claim.
- **Limits:** automatic rollback across changed owned-path sets and automatic
  downgrade of customized overlays are outside this profile. Preserve state
  and reconcile those cases manually. Outer editor/shell containment, read
  isolation, autonomous model operation and whole-task efficiency remain
  unqualified.

**Download** either the ZIP or TAR archive, plus the manifest and checksum file.
Both archives contain the same `aide-lite-pack-v0` payload. Verify its SHA-256
before use; archive identity and the exact predecessor are in the manifest.

**Provenance:** payload source `447e393b3f87004641b7387c1f33828ac1ee3a85`;
technical review `3a36366c052f308a8ecee10d32690ce0cb75cae7`;
release tag target `dfae9356241dda6a03e2cc48cf9acb245c9a6be1`.
The tag retains the qualification history for those exact payload bytes.
[Qualification evidence](https://github.com/Julesc013/aide/blob/dfae9356241dda6a03e2cc48cf9acb245c9a6be1/.aide/queue/AIDE-LITE-SUCCESSOR-QUALIFICATION-01/evidence/technical-acceptance.json)
records the tested behavior and retained failures. Its historical integration
and presentation prerequisites were subsequently resolved in
[`8fe2d12c`](https://github.com/Julesc013/aide/commit/8fe2d12cbc9d91f034cf7f68c58beda09809dc58).
Published-asset acquisition is a separate postpublication check.

Newer development features, including compact communication defaults, task
briefs, portable handoffs and outcome lessons, are reserved for a subsequent
qualified release. They are not included in these frozen 1.1.0 archives.
