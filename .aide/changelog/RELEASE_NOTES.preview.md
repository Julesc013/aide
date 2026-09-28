# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: 6a15a7dd5e3b0a8b13bf244badaab6c82f6cdf01
preview_only: true

## Highlights

- Added: Include the portable bounded job interface in the Lite release contract. (20710eace078)
- Added: Portable bounded job commands in the Lite candidate assets. (5acd32a79ab5)
- Added: Bounded attempt attribution for supplied Codex usage streams. (cec72cb6f2d7)
- Added: Candidate Lite attempt usage form with partial accounting semantics. (6a15a7dd5e3b)
- Changed: Preserve the usage repair review verdict. (8912eab9071c)
- Changed: Refresh preview metadata for the current Lite source. (65fafcc9f5be)
- Changed: Refresh unpublished Lite candidate views and qualification evidence. (65eaa5550f2e)
- Changed: Freeze reviewable current Lite candidate evidence. (a3ab41fad425)
- Changed: Record qualified local Lite candidate integration. (a468f7f038d1)
- Changed: Clarify current unpublished Lite candidate status. (0cacf2040ce8)
- Changed: Record qualified bounded execution and owned cleanup closure. (ef938eef1b78)
- Changed: Record accepted usage subtotal source review. (fe65f48c67a1)
- Changed: Schedule current usage-source release qualification. (1dada960cc47)
- Changed: Refresh unpublished release note preview. (24507295db20)
- Changed: Refresh unpublished bundle and draft views for current Lite bytes. (91cdd05776ab)
- Changed: Freeze current unpublished Lite technical effect evidence. (de308dd74462)
- Changed: Record current local technical effect acceptance. (d5a84c10b1b7)
- Changed: Record qualified local Lite effect integration. (dbf216c3e0ce)
- Changed: Record accepted portable attempt attribution source review. (6e35ea1379da)
- Changed: Refresh local Lite attribution release preview. (74c811f3b77e)
- Changed: Refresh local portable Lite pack for attempt attribution. (a233225073e7)
- Changed: Refresh local Lite stable candidate assets. (25e74785fedd)
- Fixed: Range-bound changelog provenance under mixed and open-ended selectors. (46fe61d743f0)
- Fixed: Package selected-revision changelog provenance in Lite. (f22f3ec58ed4)
- Fixed: Include selected-source changelog provenance in the local Lite candidate. (df372b3a6495)
- Fixed: Portable usage reports unknown instead of false zero or contradictory known totals. (46c51f7101c3)
- Fixed: Export corrected portable usage accounting. (640367a7b92b)
- Fixed: Include corrected usage accounting in the unpublished Lite candidate. (8f9bd0748fab)
- Fixed: Bind public Lite release claims to current candidate evidence. (ae08a6be3b96)
- Fixed: Preserve valid independent Codex usage subtotals under partial coverage. (9c391d255017)
- Fixed: Include the corrected usage subtotal importer in the portable pack. (061ef259bfca)
- Fixed: Carry corrected usage importer into local stable candidate. (2767290ac9d2)
- Fixed: Keep local preview notes bound to the exported source. (a61fc71bdc88)
- Fixed: Malformed attempt rosters now receive bounded refusal. (8f10a66b3f0a)
- Docs: Refresh the source-bound Lite release preview. (87635e1815b7)
- Docs: Bind Lite release preview to the accepted source revision. (4491c2cb8b47)

## Validation Summary

- 87635e1815b7: PASS: changelog preview reports full source_head 7a521066fdd4bf1346434d60c84090b0a63f77b2, 50 commits, and zero malformed commits in its selected range.
- 46fe61d743f0: PASS: focused selected-revision fixture regression under the approved D scratch root.
- 2c168ca172ac: PASS: all six receipt hashes matched retained D outputs; each job exited zero, was quiescent, retired scratch and released its reservation.
- 4491c2cb8b47: PASS: changelog preview reported the full selected source, 50 commits and zero malformed commits in its selected range.
- f22f3ec58ed4: PASS: D-managed export job d4b2b2278497465fb1b90feb7b12e572 exited zero, with receipt SHA-256 cfa2d4c0444314cb4df4516879c744c8977f0a250c7e881aeebf5e32acc85f45.
- df372b3a6495: PASS: D-managed stable build job 8a3ba2aa66654599b715fd50249ae1da exited zero; receipt SHA-256 d2edb9508701104066c32a57a6f7b0c3415c1b1023bac457b502b3f1d95c89a1.
- c86b7984e50b: PASS: D-managed release bundle job a90350ba8fd941bd9f7f632097da471a exited zero; receipt SHA-256 12dfd5673ed30e2b7a4cb12040e378a09809a9045804ae95413c34c7d0f8fbf1.
- 085f60c76471: PASS: D-managed draft job 90ad15e60c384907a53e4eae85fbc811 exited zero; receipt SHA-256 46f23e6a3a385181d459a4deb511c979988f2b47d7a29a065dec4716f032b6e3.
- 55131eff4af4: PASS: six current-byte consumers, 36 Q47/Q48 tests, pack/stable/preview/draft validations and zero-change postcommit replays, bound in the effect manifest.
- d489826530f0: PASS: reviewer checked four asset hashes, 18 retired receipts, 39 CLI outputs and source/artifact provenance for 55131eff.

## Known Risks

- 87635e1815b7: This is a local preview and does not publish a release or validate delivered bytes.
- 46fe61d743f0: Downstream pack, stable assets and consumers need refreshed exact-source qualification.
- 2c168ca172ac: These consumer receipts bind old bytes and do not qualify the repaired packaged script.
- 4491c2cb8b47: These reports remain preview-only and do not qualify the final pack or published release.
- f22f3ec58ed4: Stable archives and exact-byte consumer qualification must be refreshed after this pack change.
- df372b3a6495: These are local candidate bytes, not published assets or final release acceptance.
- c86b7984e50b: These outputs are local previews, not a GitHub Release or publication authorization.
- 085f60c76471: The draft is preview-only; no tag, upload or GitHub Release has been created.
- 55131eff4af4: Live one-turn model qualification and ten historical owner decisions remain pending; no main, tag or published release is claimed.
- d489826530f0: Stable publication remains REQUEST_CHANGES; this evidence commit does not alter the reviewed source or assets.

## Follow-up

- 87635e1815b7: Regenerate the pack from this committed preview, then qualify stable assets and consumer bytes.
- 46fe61d743f0: Obtain narrow source rereview, regenerate preview from this source commit, then rebuild and qualify final assets.
- 2c168ca172ac: Generate the preview at this committed head, rebuild the pack and assets, then qualify their exact bytes.
- 4491c2cb8b47: Build the pack from this preview commit, then qualify its exact stable assets.
- f22f3ec58ed4: Prove post-commit pack replay changes zero files and rebuild stable assets once.
- df372b3a6495: Prove zero-change post-commit stable replay, validate assets, then run refreshed consumers and preview projections.
- c86b7984e50b: Prove zero-change postcommit replay, validate the bundle, and refresh the local publication draft.
- 085f60c76471: Verify zero-change replay and draft validation, then freeze an exact release-effect manifest for independent review.
- 55131eff4af4: Obtain exact independent current effect review; integrate eligible source into dev, then pursue the retained external gates.
- d489826530f0: Fast-forward accepted ancestry to dev, qualify six documented portable job forms, and seek a superseding exact effect review.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
