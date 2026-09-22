# Remaining Risks And Deferrals

- Removal apply is not implemented. File deletion, directory pruning, receipt
  deletion, and managed-section removal remain separately gated.
- The plan intentionally reads only receipt-recorded managed targets. Unknown,
  target-owned, and potentially secret bytes are preserved without inspection.
- Live target use still requires target-owned authority and validation; all
  current consumer evidence comes from disposable offline fixtures.
- Proposed aliases `UR-UPDATE-06` and `UR-UPDATE-08` remain proposed; they were
  not bulk-adopted by this implementation.
- Published commit `486e81cd3a918729f28e4b452a9dcff017238a04`
  fails the current message-format checker. An exact historical disposition is
  required before the strict task-to-dev range can pass.
- Main promotion, version selection, tagging, upload, GitHub Release creation,
  downloaded-asset verification, and broader stable-profile closure remain
  separate reviewed work.
