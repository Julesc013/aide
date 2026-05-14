# Q48 Prompt Summary

Implement Q48 as AIDE's first GitHub Release Draft generator.

Q48 must generate local release-draft artifacts from the Q47 AIDE Lite release
bundle:

- GitHub release draft policies and publication-boundary rules.
- Release draft, asset, upload-plan, checklist, publication-boundary, and
  validation schemas.
- Markdown and JSON release draft outputs.
- Release asset list with checksums.
- Upload plan that is preview-only and no-upload.
- Publication checklist and publication boundary report.
- AIDE Lite release draft commands.
- Tests, golden tasks, docs, export-pack integration, validation, and evidence.

Q48 must not create tags, push tags, call GitHub APIs, create GitHub Releases,
upload assets, publish packages, mutate branches, install CI, mutate target
repositories, apply install or lifecycle plans, call providers/models, or use
network calls.
