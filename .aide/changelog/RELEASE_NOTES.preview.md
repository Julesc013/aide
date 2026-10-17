# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: 716ec1fd0ad6fb2d3875417c4db7b867a7b393fe..b5827566fbe270a604907b8c20437a1228373d81
source_head: b5827566fbe270a604907b8c20437a1228373d81
preview_only: true

## Highlights

- Changed: selected-task continuation now has source qualification evidence. (1cd847805188)
- Fixed: task resume-plan no longer declares execution safe or recommends blanket reruns. (3625acf79209)
- Fixed: portable task resume-plan preserves selected task state without claiming execution readiness. (b5827566fbe2)

## Validation Summary

- 3625acf79209: PASS: doctor, full source validation, syntax and diff checks.
- 1cd847805188: PASS: source63, actual CLI consumer, collection hashes, quiescence and retirement.
- b5827566fbe2: PASS: source63, delivered61, both CLI consumers, six ownership checks and exporter validation.

## Known Risks

- 3625acf79209: Advice cannot establish live ownership, admission, effects or evidence applicability.
- 1cd847805188: Live worker recovery, installed-host delivery and native consumer ownership remain separate.
- b5827566fbe2: Published Lite1.0.0 assets are unchanged; this is the development pack.

## Follow-up

- 3625acf79209: Qualify source and actual portable consumer, then separately review integration.
- 1cd847805188: Run reviewed portable qualification and then prepare independent integration review.
- b5827566fbe2: Run the exact reviewed preview, complete terminal review and safely synchronize dev/main.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
