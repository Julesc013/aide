# Q16 Recommendation Report

## Generated Recommendation

- ID: `REC-PROCEED-Q17-WITH-GATES`
- Evidence source: `.aide/controller/latest-outcome-report.md`
- Expected benefit: begin advisory Router Profile design after token, verifier, review, and golden-task foundations are locally healthy
- Risk level: low
- Next action: proceed to Q17 Router Profile v0 as an advisory profile only
- Rollback condition: if any controller signal regresses, pause Q17 and repair the failing local gate first
- Applies automatically: false

## Recommendation Rules Implemented

- Golden-task warning/failure recommends repairing quality gates before promotion.
- Packet over-budget or token regression recommends context/packet tightening.
- Verifier WARN/FAIL recommends repairing evidence or verifier issues before review.
- Incomplete review packet recommends rerunning `review-pack` or repairing the template/evidence refs.
- Missing or stale context artifacts recommend rerunning `snapshot`, `index`, and `context`.
- Adapter drift recommends rerunning `adapt`.
- All core signals passing recommends Q17 Router Profile v0 as advisory-only work.

## Safety Notes

No recommendation mutates files, prompts, policies, routes, provider settings, or generated artifacts automatically. Implementation requires a future queue item or explicit human approval.
