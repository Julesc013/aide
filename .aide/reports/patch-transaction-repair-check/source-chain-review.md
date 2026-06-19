# Source Chain Review

The live source chain satisfies the repair-check gate.

- Live branch: `main`.
- Live head: `fca99236c2f933660de29b657dc181f1174dd719`.
- Original build commit: `2559b1dbc528992451193d942bff741e8cb0a0a7`.
- Original failed-check commit: `83565996d277e0eff07447333c2aea0a726932e6`.
- Initial repair commit: `f5422fb150da85d00f768e92c718b2b7336a502c`.
- Latest repair hardening commit:
  `fca99236c2f933660de29b657dc181f1174dd719`.

`AIDE-CHECK-PATCH-TRANSACTION-SCHEMA-01` remains preserved with
`FAILED_VALIDATION` and identifies the two material path-scope defects. The
repair task reports `PASS_WITH_WARNINGS`, `missing_evidence: 0`, and recommends
this repair check.

No later repair-check or superseding PatchTransaction repair was found in live
queue truth during this run.
