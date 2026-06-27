# Remaining Risks

- UpdateReceipt v0 remains proposed until `AIDE-ACCEPT-UPDATE-RECEIPT-V0-01` completes.
- DistributionApplyEngine remains not started and must not rely on UpdateReceipt until acceptance completes.
- Positive fixture rows do not individually exercise every operation receipt class and skipped-operation reason, though the schema/helper validates the full enum surfaces.
- Future fixture-only apply-engine work must keep real target mutation, release publication, provider/model/network calls, and canaries out of scope until explicitly authorized.
