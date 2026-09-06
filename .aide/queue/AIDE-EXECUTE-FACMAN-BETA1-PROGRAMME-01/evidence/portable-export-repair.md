# Portable export repair

Initial validation failed on mismatched sanitized local-state example checksums and an omitted example secrets/README.md. Regenerating the official pack reconciles current portable source and payload hashes. The omitted README contains only instructions forbidding real secrets; it must be explicitly tracked despite the generic ignore rule.

Regeneration exposed a second defect: recursive test-directory inclusion exported source-only runtime tests into targets without their source-only core modules. The bounded source filter retains every previously admitted AIDE-named portable test (three exact paths), excludes full-source AIDE/continuous-worker test modules throughout that subtree, and has positive/negative/nested regression coverage. No controller source, source queue, runtime host or live authority is imported into FacMan.

The eleven-file prototype manifest remains 9340793dac9777ae137fbc1c060b2d9c10383cfc761e15258f3f578f51b0cdee. Export/queue integration does not establish live worker qualification. Final staged payload hashes must match the portable checksum manifest before integration, and required command results are recorded separately.
