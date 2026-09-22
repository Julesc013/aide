# Independent Release Integrity Rereview

## Decision

`REQUEST_CHANGES`

The independent reviewer examined exact commit
`9f4bbc0a77443bd84a5c2502882e95aa602f98fe`, tree
`af019b3fffbc0d8b27b3db60082ae0e80067e754`, against exact base
`cc85be9c472a16f39aae98ba00fd5de145098862`.

## Findings

1. `HIGH`: deleting either paired changelog JSON source allowed the Markdown
   preview to remain source-bound and publish-candidate. Bundle, validation,
   draft, and draft validation all passed in the disposable reproduction.
2. `MEDIUM`: projection commit `198a87d2` still named superseded local
   checkpoint `75e37a4c` in its message even though its actual parent is the
   tree-equivalent policy-correct checkpoint `dd1f39f3`.

## Prior Finding Dispositions

- Malformed and mismatched preview JSON refusal: closed.
- Missing paired preview JSON refusal: open at the reviewed commit.
- Git replacement-object ancestry defense: closed.
- Committed artifact/projection convergence: closed for trees and bytes.

## Independent Verification

- 58 unit tests passed with no failures or skips.
- Complete bundle, validate, draft, and draft-validate replay passed and left a
  clean tree.
- Pack status, canonical validate, doctor, commit-range policy, and diff checks
  passed.
- All audited export, archive, release, asset-index, and provenance hashes
  matched actual bytes.
- No machine-local path leak, tag, upload, GitHub Release, or enabling release
  claim was found.

## Required Repair

Require both preview representations to exist, parse, and agree; add deletion
regressions through the release draft boundary; regenerate a new source,
artifact, and projection chain whose messages bind actual parent identities;
then obtain a superseding exact rereview.

This review does not authorize dev integration, main promotion, tagging,
upload, or publication.
