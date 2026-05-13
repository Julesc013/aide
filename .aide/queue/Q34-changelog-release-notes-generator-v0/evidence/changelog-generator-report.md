# Changelog Generator Report

Status: complete for review.

- policy: `.aide/policies/changelog.yaml`
- config: `.aide/changelog/config.yaml`
- templates: `.aide/changelog/templates/changelog.md.template`, `.aide/changelog/templates/release-notes.md.template`
- commands: `changelog preview`, `changelog validate`, `changelog status`
- source range: `HEAD latest 50 commits`
- source head: `453fe6aa9d6676dbfd4ae3a7b0dc826498f5f7eb`
- commit count: 50
- entry count: 77
- malformed count: 13
- category counts: Added 8, Changed 7, Fixed 5, Docs 8, Tests 14, Internal 27, Risks 6, Follow-up 2

The generator reports malformed/legacy commits but returns success when preview files are structurally valid. No tags, publishing, branch mutation, provider/model calls, or network calls are performed.
