# Source Chain Review

The live source chain satisfies the repair baseline:

- `AIDE-BUILD-MCP-SERVER-CONTRACT-01` exists and is complete at
  `needs_review`.
- Build result is `PASS_WITH_WARNINGS`.
- Build evidence reports `missing_evidence: 0`.
- `AIDE-CHECK-MCP-SERVER-CONTRACT-01` exists and is complete at
  `needs_review`.
- Check result is `FAILED_VALIDATION`.
- Check evidence reports `missing_evidence: 0`.
- Build commit `c8a143f76af585ae3a0cc3004fb5278c57f264e0` is an ancestor of
  live HEAD.
- Failed-check commit `18839ccf9b1ec2b129064b09bfb2c90988e31e63` is live HEAD
  at task start.
- No later MCP repair or superseding MCP task existed before this repair was
  registered.
