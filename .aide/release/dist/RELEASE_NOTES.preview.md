# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 8912eab9071cd2599fb4f43721aa0dafea807a8e latest 50 commits
source_head: 8912eab9071cd2599fb4f43721aa0dafea807a8e
preview_only: true

## Highlights

- Added: Explicit one-turn Codex job adapter in the existing Lite runner. (651744c0a428)
- Added: Include the portable bounded job interface in the Lite release contract. (20710eace078)
- Added: Portable bounded job commands in the Lite candidate assets. (5acd32a79ab5)
- Changed: Preserve Codex worker one-turn result qualification. (7eaebe3bec42)
- Changed: Retain Codex worker result boundary qualification. (9fe9cb485daf)
- Changed: Record reviewed Codex result boundary integration. (e447e6416b74)
- Changed: Retain Codex usage import qualification. (e5bb4f8b53ca)
- Changed: Record portable Codex usage repair integration. (326492ff6df6)
- Changed: Codex host source qualification and remaining gates. (6281a6b903ca)
- Changed: Durable dev integration record for Codex host source. (38fbe92266bd)
- Changed: Extracted Lite fixture covers Codex permission refusal. (1bacae3a9be0)
- Changed: Durable delivered Codex admission test evidence. (12351b07c340)
- Changed: Current Lite pack refresh execution plan. (6c4f61553495)
- Changed: Current-source Lite portable pack candidate. (c22d41112973)
- Changed: Current Lite pack uses repaired non-circular provenance. (a7ab0223d1ba)
- Changed: Local Lite 1.0.0 candidate includes current portable source. (b147aa8cf28a)
- Changed: Preserve the usage repair review verdict. (8912eab9071c)
- Fixed: Bind worker verdicts and usage to one observed Codex turn. (9dccd27fe2f3)
- Fixed: Keep the turn-boundary regression focused on refusal. (1497a7e2ad4f)
- Fixed: Codex worker result binding to the final item and unique JSON fields. (2086e512aeb3)
- Fixed: Refuse ambiguous Codex usage import fields. (8a12605dc1af)
- Fixed: Pause-aware one-turn Codex job dispatch. (e9fce7a9c1a4)
- Fixed: Reject ambiguous Lite job dispatch state. (1105ad98e516)
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
- Docs: Refresh the source-bound Lite release preview. (87635e1815b7)
- Docs: Bind Lite release preview to the accepted source revision. (4491c2cb8b47)

## Validation Summary

- 9dccd27fe2f3: PASS: AST parse of the three Python files and diff whitespace check.
- 1497a7e2ad4f: FAIL retained: First D-managed state suite passed 22/23; this assertion alone failed.
- 7eaebe3bec42: FAIL retained: Initial state suite 22/23 from an over-specific oracle message.
- 2086e512aeb3: PASS: git diff --check.
- 9fe9cb485daf: PASS: D-managed state 26/26 and pipeline 32/32 at source 2086e512.
- e447e6416b74: PASS: git ls-remote matched local and remote-tracking dev at 9fe9cb48.
- 8a12605dc1af: PASS: git diff --check.
- e5bb4f8b53ca: PASS: D-managed focused suite 15/15 at source 8a12605d.
- 326492ff6df6: PASS: git ls-remote matched local and remote-tracking dev at e5bb4f8b.
- 651744c0a428: PASS: git diff --check.

## Known Risks

- 9dccd27fe2f3: Live Codex effect and exported Lite behavior remain unqualified.
- 1497a7e2ad4f: Production worker parser is unchanged by this test-only correction.
- 7eaebe3bec42: No real Codex turn or Lite export was qualified by these synthetic tests.
- 2086e512aeb3: Synthetic parser tests do not qualify a live Codex model turn.
- 9fe9cb485daf: No live Codex model turn or portable Lite release was qualified.
- e447e6416b74: No live Codex turn or stable release qualification was performed.
- 8a12605dc1af: Synthetic records do not establish actual host usage coverage.
- e5bb4f8b53ca: No live host usage or stable release bytes were qualified.
- 326492ff6df6: No real model call or stable asset qualification was performed.
- 651744c0a428: No live model effect, pause-aware dispatch or delivered-byte qualification yet.

## Follow-up

- 9dccd27fe2f3: Run state and pipeline suites through the D owner; seek independent exact source review.
- 1497a7e2ad4f: Rerun exact state suite, then pipeline suite under the D owner.
- 7eaebe3bec42: Obtain independent exact source and scope review before dev integration.
- 2086e512aeb3: Run D-managed suites and obtain independent review of this repair before dev integration.
- 9fe9cb485daf: Integrate accepted source into dev; retain separate real-effect and release gates.
- e447e6416b74: Qualify the real permitted worker effect and delivered Lite behavior separately.
- 8a12605dc1af: Run the D-managed focused suite and obtain exact source review before dev.
- e5bb4f8b53ca: Fast-forward reviewed source into dev and observe the remote ref.
- 326492ff6df6: Qualify the host binding and current delivered Lite candidate separately.
- 651744c0a428: Test source under D owner, close pause race and obtain independent review before dev.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
