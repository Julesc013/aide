# Exact owner decision packet

The mechanism source at `59b886db` has a fresh `ACCEPT_WITH_NOTES` review.
This packet asks the responsible owner for three independent historical-message
decisions. A source review is not a decision on any record. The registry still
marks all three `proposed`, so raw and default checks still fail.

| Choice | Exact commit | Disposition id | Original message failure |
| --- | --- | --- | --- |
| A | `bfb86c12b9e6d2970024d29c57ba629994ec43cc` | `bfb86c12-historical-validation-token` | One missing recognized validation outcome token |
| B | `486e81cd3a918729f28e4b452a9dcff017238a04` | `486e81cd-historical-structured-body` | Thirteen missing bullet, changelog category, and trailer forms |
| C | `1011d008fc39b135a5ef27062b5b8ee9c95cdc7f` | `1011d008-api-query-why-bullet` | One missing `## Why` bullet form |

For each choice, the owner may answer `accept` or `reject`. Accept means only
that the exact immutable message failure may be dispositioned for range
integration checks after a structured exact decision file and registry record
are reviewed and committed. It does not turn the raw message into `PASS`,
accept product functionality, authorize native/hosted effects, or promote or
publish a release. Reject leaves the exact range failure in force. An omitted
choice stays proposed; silence and broad campaign authorization have no effect.

An accepted decision artifact must name the exact disposition id, commit,
tree, message hash, scope, decision, `owner:Julesc013`, and review date, then
match the registry by content hash. Proposed records already bind ordered
parents, exact failed checks, evidence digest, and record digest. The raw
failure details and object identities are in `raw-policy-failures.md` and the
source registry. The source-specific registry is excluded from portable packs.

Requested response format: `A accept/reject; B accept/reject; C accept/reject`.
