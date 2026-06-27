# Validation

The build validates UpdateReceipt v0 as a proposed no-apply receipt object.

The projection and validation reports are under `.aide/reports/update-receipt-v0/**`.

The focused fixture matrix covers valid receipt cases, preservation receipts, skipped and refused operations, optional extension preservation, and invalid fail-closed cases for missing refs, unplanned operations, digest mismatches, unsafe ownership changes, authority claims, unsafe paths, source latest output misuse, and unknown required features.
