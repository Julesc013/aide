# Source Selection Review

The ContextPack v2 projection references bounded source and report files by
repo-relative path and sha256. It does not inline raw repository dumps or resolve
external resources.

Selected source classes include:

- resume AdapterManifest acceptance status and reports
- original blocked ContextPack status
- current ContextPack resume-build status
- PatchTransaction resume acceptance report
- ConformanceResult acceptance and validation reports
- CapabilityManifest validation report
- Reconciler validation report
- OKF knowledge index
- `PLANS.md` and `IMPLEMENT.md`

Generated projection count:

- source refs: 13
- sections: 8
