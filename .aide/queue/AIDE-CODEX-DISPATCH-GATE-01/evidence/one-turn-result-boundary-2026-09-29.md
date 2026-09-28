# One-turn Codex worker result boundary

Date: 2026-09-29. Candidate branch `task/aide-codex-result-boundary-01` from `dev@31107d1854e64a237514babc2e406a064b470866`. Source/parser commit `9dccd27fe2f3318765fb4200e584221e42409cb4`, tree `68ec9f8ea9ec3d6b9fb8072392a8937ee2738fb2`; test-oracle-only correction `1497a7e2ad4f54db6d4ee5050907207885b9fd62`, tree `76e0316d8ab38d95c956ea7eadf4673120b624ec`.

The worker now refuses a Codex JSONL verdict without one ordered thread start, turn start, final agent message and turn completion. Duplicate starts/completions, a message outside the active turn, noncanonical or malformed session UUID, and non-object usage are refused. The one-turn source boundary does not infer the number of internal model requests from CLI events.

First D-managed state suite at `9dccd27f`: **22/23**, exit 1, job `4c844159fe714092a098ee96cc563fbf`, receipt SHA-256 `6689c9a5f9710bdc2d462c50fccd3f9a9c1606e26a72bd2a403ccc04ebb97e1c`. The missing-turn case was correctly refused, but its test expected a different message. The failure remains a failed attempt; no production source changed in the correction.

Superseding D-managed source-bound jobs at `1497a7e2`:

- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_state.py -v`: **23/23 PASS**, exit 0, job `c24fae14ab1e406cb94a8613eeb4fb81`, manifest digest `ac195b6c60e3baa1eb6259299be9878b66ffc58a65b253071f9479f69bbfdb71`, receipt SHA-256 `3785b49cfee9df0a513da5f76c7ef1fd872274412121f1b581289ff21c0d6f08`.
- `python -m unittest discover -s .aide/scripts/tests -p test_continuous_worker_pipeline.py -v`: **32/32 PASS**, exit 0, job `ecb784392ef748809c6446e27ebe26e1`, manifest digest `2b159eceb7228f01b8a236b9bb3c190bac400c8ca0e3b45cb3dcd1fa6c3e33d4`, receipt SHA-256 `58d6213c9a2bc560431379776f65782318b40f13d2b89a80695a8e596987f9d6`.

All three retained receipts say `retired`, scratch absent and reservation released; the exact scratch children were also checked absent. The pipeline uses synthetic Codex JSONL and the installed CLI's no-model version launch. These are source and test results, not a live Codex turn, hosted qualification, Lite export or release acceptance. Independent review of the exact source and scope amendment remains required before dev integration.
