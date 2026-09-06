# Provider closeout evidence custody

The current task status and integration plan record the completed provider chain.
They do not claim FacMan pin adoption or operational broker qualification.

`provider-closeout-evidence.zip` preserves original byte streams for the provider
receipts, helper logs and pre-closeout metadata. `provider-closeout-custody.json`
binds every member and distinguishes original hashes from Git LF text projections.
Paths beginning `evidence/provider-source/` or `evidence/historical-before-closeout/`
in imported receipts resolve to identically named ZIP members after checkout.
Original loose raw files remain on the authoring machine, unstaged.

The provider-wide 196-path manifest is preserved verbatim in each ZIP as
`aide-provider-closeout-changed-bytes.json`. Essential current summary documents
are also archived before Git normalization. Hash references in historical receipts
must be checked against ZIP bytes.

Exact canonical chain members:

- `evidence/provider-source/usk-streaming-integration-chain.json` (`5d13722796bd64a7c5098bb24ace07ae530a1925e5c7a1c007ad02475fb0066c`).
- `evidence/provider-source/pr27-canonical-promotion-chain.json` (`f7fea3ad8727699fc91dcb4c5de5aabd27a762470e9bc9cb8a9e155484608085`).
