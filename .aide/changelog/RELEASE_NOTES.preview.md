# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 1dada960cc47189e8a1c21be87b41aed02ea835a latest 50 commits
source_head: 1dada960cc47189e8a1c21be87b41aed02ea835a
preview_only: true

## Highlights

- Added: Include the portable bounded job interface in the Lite release contract. (20710eace078)
- Added: Portable bounded job commands in the Lite candidate assets. (5acd32a79ab5)
- Changed: Codex host source qualification and remaining gates. (6281a6b903ca)
- Changed: Durable dev integration record for Codex host source. (38fbe92266bd)
- Changed: Extracted Lite fixture covers Codex permission refusal. (1bacae3a9be0)
- Changed: Durable delivered Codex admission test evidence. (12351b07c340)
- Changed: Current Lite pack refresh execution plan. (6c4f61553495)
- Changed: Current-source Lite portable pack candidate. (c22d41112973)
- Changed: Current Lite pack uses repaired non-circular provenance. (a7ab0223d1ba)
- Changed: Local Lite 1.0.0 candidate includes current portable source. (b147aa8cf28a)
- Changed: Preserve the usage repair review verdict. (8912eab9071c)
- Changed: Refresh preview metadata for the current Lite source. (65fafcc9f5be)
- Changed: Refresh unpublished Lite candidate views and qualification evidence. (65eaa5550f2e)
- Changed: Freeze reviewable current Lite candidate evidence. (a3ab41fad425)
- Changed: Record qualified local Lite candidate integration. (a468f7f038d1)
- Changed: Clarify current unpublished Lite candidate status. (0cacf2040ce8)
- Changed: Record qualified bounded execution and owned cleanup closure. (ef938eef1b78)
- Changed: Record accepted usage subtotal source review. (fe65f48c67a1)
- Changed: Schedule current usage-source release qualification. (1dada960cc47)
- Fixed: Bounded Windows checkpoint retry under reader contention. (12ac93c9aeec)
- Fixed: Codex host admission and bounded retained input. (36c944159c09)
- Fixed: Setup quota regression expectation. (33151c5ea97c)
- Fixed: Ambiguous local Codex model permissions now fail closed. (67e1d572d513)
- Fixed: Delivered host refusal oracle now covers run admission. (8b0cba063b37)
- Fixed: Non-circular portable pack provenance replay. (86838e444162)
- Fixed: Changelog preview provenance for explicit historical revisions. (7a521066fdd4)
- Fixed: Range-bound changelog provenance under mixed and open-ended selectors. (46fe61d743f0)
- Fixed: Package selected-revision changelog provenance in Lite. (f22f3ec58ed4)
- Fixed: Include selected-source changelog provenance in the local Lite candidate. (df372b3a6495)
- Fixed: Portable usage reports unknown instead of false zero or contradictory known totals. (46c51f7101c3)
- Fixed: Export corrected portable usage accounting. (640367a7b92b)
- Fixed: Include corrected usage accounting in the unpublished Lite candidate. (8f9bd0748fab)
- Fixed: Bind public Lite release claims to current candidate evidence. (ae08a6be3b96)
- Fixed: Preserve valid independent Codex usage subtotals under partial coverage. (9c391d255017)
- Docs: Refresh the source-bound Lite release preview. (87635e1815b7)
- Docs: Bind Lite release preview to the accepted source revision. (4491c2cb8b47)

## Validation Summary

- 12ac93c9aeec: FAIL retained: 40/41 D-managed cases at 1105ad98 due to active.json.next contention.
- 36c944159c09: PASS: git diff --check.
- 33151c5ea97c: FAIL retained: 44/45 D-managed cases at 36c94415; one stale fixture expectation.
- 67e1d572d513: PASS: git diff --check.
- 6281a6b903ca: PASS: final source 67e1d572 D-managed 46/46 synthetic cases, job 5e5972bf; reviewer ACCEPT for dev source only.
- 38fbe92266bd: PASS: git plan dry-run; commit check dev..HEAD 8/8; remote dev observed at 6281a6b9.
- 1bacae3a9be0: PASS: git diff --check.
- 8b0cba063b37: PASS: git diff --check.
- 12351b07c340: PASS: 1/1 extracted fixture at 8b0cba06 in D job dabd6ae6; reviewer ACCEPT for dev test only.
- 6c4f61553495: PASS: git diff --check; plan only, generator not yet run.

## Known Risks

- 12ac93c9aeec: Persistent replacement failure still requires explicit recovery and remains a failure.
- 36c944159c09: The local executable path remains trusted against hostile same-user mutation between the final hash and CreateProcessW.
- 33151c5ea97c: The full focused suite remains pending after this fixture correction.
- 67e1d572d513: Same-user hostile mutation between final executable hash and CreateProcessW remains outside this local binding guarantee.
- 6281a6b903ca: Live Codex turn, JSONL verdict, exported Lite and final release qualification remain open.
- 38fbe92266bd: This evidence-only closeout does not qualify live model output or final distribution bytes.
- 1bacae3a9be0: This test does not launch a model or prove a JSONL result.
- 8b0cba063b37: No live model or JSONL verdict is exercised by this synthetic refusal.
- 12351b07c340: No live model, JSONL verdict or canonical release bytes were qualified.
- 6c4f61553495: Live model turn and historical promotion decisions remain pending.

## Follow-up

- 12ac93c9aeec: Rerun exact managed suite and seek independent source review.
- 36c944159c09: Run the D-managed suite, preserve the review result, and qualify the final combined source.
- 33151c5ea97c: Rerun the D-managed suite and seek scoped independent rereview.
- 67e1d572d513: Run the D-managed suite and close the exact review before dev integration.
- 6281a6b903ca: Integrate accepted source in dev and qualify actual combined and delivered behavior.
- 38fbe92266bd: Qualify the current extracted Lite host path and bounded JSONL verdict.
- 1bacae3a9be0: Run the exact delivered fixture and retain its result before dev integration.
- 8b0cba063b37: Rerun the exact consumer and close the narrow review.
- 12351b07c340: Integrate accepted test and continue actual host/release qualification.
- 6c4f61553495: Run the admitted export job once, validate and commit coherent generated bytes.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
