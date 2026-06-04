# Validation Matrix

| Surface | Validator behavior | Evidence |
| --- | --- | --- |
| lifecycle schemas | Parse known schema files, require root objects, required arrays, `schema_version` consts, and `needs_review` gates. | `.aide/reports/lifecycle-schema-validation.md` |
| lifecycle examples | Parse known examples, require schema versions, example flags, required fields, fixture-only target class, and honest capability labels. | `.aide/reports/lifecycle-schema-validation.md` |
| non-mutating examples | Require report/dry-run modes, false mutation flags, empty changed-file lists, and no enabled target mutation. | `.aide/reports/lifecycle-schema-validation.md` |
| path boundaries | Reject absolute paths, path traversal, and protected target paths in target path fields. | targeted unit tests |
| operation allowlist | Allow only `update_managed_section`, `report`, `validate`, and `noop` in examples. | targeted unit tests |
| rollback-compatible record | Require rollback evidence shape and `rollback_execution_implemented: false`. | `.aide/reports/lifecycle-schema-validation.md` |
| fixture shape | Validate fixture root shape without materializing target files. | `.aide/reports/lifecycle-schema-fixture-validation.md` |
| capability reality | Keep lifecycle capability review-gated, not production-ready or release-ready. | status/evidence |
