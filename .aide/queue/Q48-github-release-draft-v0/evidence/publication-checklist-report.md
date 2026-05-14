# Q48 Publication Checklist Report

## Outputs

- Markdown: `.aide/release/github-release-checklist.md`
- JSON: `.aide/release/github-release-checklist.json`

## Checklist Summary

- Blockers: 0
- Warnings: inherited release/source warnings only.
- Manual review items: 7
- `no_publish`: true

## Required Manual Review Items

- Review release body.
- Review suggested tag.
- Review asset list.
- Review known risks.
- Review target install caveats.
- Decide whether a future release is pre-release, draft, or stable.
- Decide whether to publish in a future explicit phase.

## Publication Blocker Rules

The checklist treats failed validation, missing artifacts, missing checksums,
secret findings, unaccepted dirty state, or target install claims without target
proof as publication blockers.

## Result

The checklist is generated and reviewable. It does not publish, tag, upload, or call GitHub.
