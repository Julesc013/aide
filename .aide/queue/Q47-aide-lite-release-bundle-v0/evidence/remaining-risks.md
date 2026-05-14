# Remaining Risks

- Q47 produces local release artifacts only; no public GitHub Release draft or publication exists yet.
- The installer remains observe/plan/dry-run only. There is still no apply-mode install/repair/upgrade/rollback/uninstall path.
- Target repos such as Dominium and Eureka must generate their own install, upgrade, repair, rollback, and validation evidence after importing or extracting a pack.
- Changelog preview still records 15 historical malformed commits. Q47 bundles the preview and records the warning; it does not rewrite history.
- Release provenance records dirty source state because generated Q47 artifacts and evidence existed during local bundling. This is intentional evidence, not publication approval.
- Archive filtering now excludes forbidden local-state paths from release archives; future export-pack changes should keep release archive validation in the loop.
- Q48 is still required to create a reviewed GitHub Release Draft model before any public release workflow is considered.
