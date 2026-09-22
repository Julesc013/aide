# Exact Historical-Disposition Decision Request

Date: 2026-09-22
Task: `AIDE-HISTORICAL-COMMIT-DISPOSITIONS-01`

## Decision Subject A

- Disposition id: `bfb86c12-historical-validation-token`
- Exact commit: `bfb86c12b9e6d2970024d29c57ba629994ec43cc`
- Requested decision: accept only the recorded historical commit-message
  nonconformance for range integration checks.
- Basis: the original message is structured and source/tree identity is
  preserved, but its validation prose predates the recognized uppercase
  outcome token requirement.
- Excluded: declaring the original message conformant, inventing a historical
  test result, changing the commit, accepting adjacent commits, or approving a
  main promotion.

## Decision Subject B

- Disposition id: `486e81cd-historical-structured-body`
- Exact commit: `486e81cd3a918729f28e4b452a9dcff017238a04`
- Requested decision: accept only the recorded historical commit-message
  nonconformance for range integration checks.
- Basis: the commit was published before the strict message failure was found;
  the delivered-pack removal behavior has separate test and artifact evidence,
  while the original message omits the currently required bullet/category and
  trailer forms.
- Excluded: treating message disposition as product qualification, changing
  the commit, accepting adjacent commits, integrating the product branch, or
  approving a main promotion.

## Available Decisions

The responsible owner or reviewer may independently choose `accepted` or
`rejected` for each exact subject. Silence, broad campaign authorization, and
the existence of this packet leave both entries `proposed` and ineffective.

For acceptance, the registry must record an `owner:` or `reviewer:` identity,
the exact review date, this decision file's content digest, the raw-evidence
file's content digest, and a recomputed record digest. The checker then still
prints every original failure and reports `DISPOSITIONED`, not `PASS`, for the
historical commit.

## Safety Boundary

- The source-specific registry is excluded from portable AIDE packs.
- Latest-commit, message-file, and hook checks remain strict.
- Wildcards, prefixes, blanket merge exemptions, missing evidence, stale
  hashes, duplicate records, and malformed accepted records fail closed.
- This decision does not authorize main promotion, tagging, upload,
  publication, hosted effects, permission changes, or history rewriting.
