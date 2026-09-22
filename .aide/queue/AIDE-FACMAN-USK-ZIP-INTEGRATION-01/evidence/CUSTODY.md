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

- `evidence/provider-source/pr28-canonical-integration-chain.json` (`7684353e5ad61ff5fd8446c277dae40a10b022400c4f9c5a9400f3a99190dc60`).
- `evidence/provider-source/path-admission-canonical-integration-chain.json` (`149351d0aae2f6965614b602ddafa82358966be03a34e5926ba146f7f65dfda6`).
