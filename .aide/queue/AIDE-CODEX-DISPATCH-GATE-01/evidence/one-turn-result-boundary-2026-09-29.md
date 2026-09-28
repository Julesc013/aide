# One-turn Codex worker result boundary

Date: 2026-09-29. Candidate branch `task/aide-codex-result-boundary-01` from `dev@31107d1854e64a237514babc2e406a064b470866`. Source/parser commit `9dccd27fe2f3318765fb4200e584221e42409cb4`, tree `68ec9f8ea9ec3d6b9fb8072392a8937ee2738fb2`; test-oracle-only correction `1497a7e2ad4f54db6d4ee5050907207885b9fd62`, tree `76e0316d8ab38d95c956ea7eadf4673120b624ec`.

The worker now refuses a Codex JSONL verdict without one ordered thread start, turn start, final agent message and turn completion. Duplicate starts/completions, a message outside the active turn, noncanonical or malformed session UUID, and non-object usage are refused. The one-turn source boundary does not infer the number of internal model requests from CLI events.

First D-managed state suite at `9dccd27f`: **22/23**, exit 1, job `4c844159fe714092a098ee96cc563fbf`, receipt SHA-256 `6689c9a5f9710bdc2d462c50fccd3f9a9c1606e26a72bd2a403ccc04ebb97e1c`. The missing-turn case was correctly refused, but its test expected a different message. The failure remains a failed attempt; no production source changed in the correction.

Superseding D-managed source-bound jobs at `1497a7e2`:

- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_state.py -v`: **23/23 PASS**, exit 0, job `c24fae14ab1e406cb94a8613eeb4fb81`, manifest digest `ac195b6c60e3baa1eb6259299be9878b66ffc58a65b253071f9479f69bbfdb71`, receipt SHA-256 `3785b49cfee9df0a513da5f76c7ef1fd872274412121f1b581289ff21c0d6f08`.
- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_pipeline.py -v`: **32/32 PASS**, exit 0, job `ecb784392ef748809c6446e27ebe26e1`, manifest digest `2b159eceb7228f01b8a236b9bb3c190bac400c8ca0e3b45cb3dcd1fa6c3e33d4`, receipt SHA-256 `58d6213c9a2bc560431379776f65782318b40f13d2b89a80695a8e596987f9d6`.

All three retained receipts say `retired`, scratch absent and reservation released; the exact scratch children were also checked absent. The pipeline uses synthetic Codex JSONL and the installed CLI's no-model version launch. These are source and test results, not a live Codex turn, hosted qualification, Lite export or release acceptance. Independent review of the exact source and scope amendment remains required before dev integration.

## Independent finding and superseding repair

Reviewer `/root/native_os_build_review` returned **REQUEST_CHANGES** on source `9dccd27f` through evidence HEAD `7eaebe3b`. Two read-only in-memory reproductions showed that a completed `pass` message followed by a failed command item still returned `pass`, and that duplicate `status` keys in final JSON could replace `fail` with `pass`. The 23/23 and 32/32 jobs above predate this finding and do not qualify the repair.

Superseding source/test commit `2086e512aeb3c8050451a5308b549c2839e4d245`, tree `58ee78586139888e6354d953bf0bde54eb6c225f`, invalidates an earlier message on later item activity and refuses duplicate object keys in outer events and final verdict JSON. Focused regressions cover both reproductions and a new final message after intervening activity.

Sequential D-managed jobs bound to that exact commit/tree:

- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_state.py -v`: **26/26 PASS**, exit 0, job `7d64507d36644192bccb8253e627dd31`, manifest digest `5f75df984105591b250e48f4f181c297f7e87c252b5de417b0132c3cb207534f`, receipt SHA-256 `8006e68f3b1982693df37a9e393c645c791394c1febd13d05baece202d9529a2`.
- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_pipeline.py -v`: **32/32 PASS**, exit 0, job `c22f0a7bf534447f883aa313f1fc4203`, manifest digest `2a9d6409f22f1fa2f0af4b9e450fa973aaccaeb5770e755007087659c8182292`, receipt SHA-256 `b07e4cd512600e4b4cbd031f2c9209d68c4873978542b26be0f08c4634ab30fa`.

Both receipts record `retired`, scratch absent and reservation released; exact scratch children were checked absent. Peak memory was 24,236,032 and 126,844,928 bytes respectively; peak scratch was 3,545 and 1,386,720 bytes. These remain synthetic, no-model tests.

Independent reviewer `/root/native_os_build_review` returned **ACCEPT** for the scoped rereview of exact source `2086e512aeb3c8050451a5308b549c2839e4d245`, tree `58ee78586139888e6354d953bf0bde54eb6c225f`, relative to rejected evidence HEAD `7eaebe3b`. The reviewer confirmed later item activity invalidates the old message and duplicate object keys are refused, checked `git diff --check`, and did not rerun suites or call a live model. The reviewer noted a malformed completed item lacking `item` can raise `KeyError`; the coordinator catches it and blocks, so this is not a pass acceptance. Verdict scope is dev source integration only; real Codex effect, portable Lite and release qualification remain open.

`dev` fast-forwarded from `31107d1854e64a237514babc2e406a064b470866` to reviewed-evidence HEAD `9fe9cb485daf8ef6e1dbbabc876a6346e12899e5`, tree `a4928b888c762a85829db5a5faf2eddc26c5e149`. The exact `origin/dev` ref and `git ls-remote --heads origin dev` both returned `9fe9cb485daf8ef6e1dbbabc876a6346e12899e5`. The source tests remain bound to `2086e512`; evidence-only commits did not change parser or test bytes.
