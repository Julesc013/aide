# Identity, References, and Digests

| Field | Value |
|---|---|
| Contract status | Adopted desired-state contract |
| Source family | S21 identity and byte contract, adapted to live AIDE records |
| Implementation | Partial across source, Git, queue, and evidence records |
| Behavioral qualification | Not established by this document |
| Owner | Protocol owner for each identity namespace |

## Principle

Logical identity, revision, location, version, and integrity are related but
different dimensions. A stable logical object may move. A content change creates
a different revision or digest even when its path does not change.

References must carry enough context to be interpreted safely. A Git object ID
needs its algorithm and repository context. A path needs its root and path
profile. An interchange URI is not automatically a filesystem path, authority
token, or executable locator.

This contract introduces desired invariants. It does not migrate existing IDs,
rename established files, or make a candidate source identifier authoritative.

## Digest and Lineage Boundaries

A trust-bearing digest must define the exact bytes, algorithm, media type, and
canonicalization profile. Raw-byte and semantic digests have different uses.
Changing a serializer or canonicalizer cannot silently revalidate old evidence
under a new profile.

Line numbers alone are not permanent symbol identities. Declared moves, exact
matches, and inferred successors must remain distinguishable. Ambiguous splits
or mergers stay ambiguous unless an owner records lineage. A reference alias
does not by itself provide an import shim, redirect, or migration.

Signed payloads, endorsements, and display renderings are separate objects. A
review record must not circularly include its own mutable endorsement bytes in
the digest it claims to endorse.

## Requirements

### AIDE-ID-001: Distinct Identity Dimensions

Records MUST distinguish logical identity, exact revision, current locator,
and artifact digest when those dimensions apply.

### AIDE-ID-002: Namespaced Source IDs

Imported requirement and decision identifiers MUST be namespaced by exact
source identity before deduplication or aliasing.

### AIDE-ID-003: Qualified Digests

Every trust-bearing digest MUST declare its algorithm and byte or
canonicalization profile.

### AIDE-ID-004: Historical Verification

Supported historical digest and schema profiles MUST remain verifiable or
return an explicit unsupported result.

### AIDE-ID-005: Safe Locators

Resource resolution MUST enforce explicit root, path, scheme, and permission
rules rather than treating an identifier as an executable path.

### AIDE-ID-006: Honest Lineage

File and symbol lineage MUST classify exact matches, declared moves, and
inferred successors separately.

### AIDE-ID-007: No Circular Approval Digest

Review and signature records MUST bind a separately defined payload and MUST
NOT depend circularly on their own mutable endorsement bytes.

## Acceptance Direction

Acceptance should cover a byte-preserving rename, colliding source-local IDs,
serializer changes, historical canonicalizers, path traversal through a
locator, ambiguous symbol splits, and an endorsement appended after payload
creation.

These are desired acceptance cases. This document records none of them as run.
