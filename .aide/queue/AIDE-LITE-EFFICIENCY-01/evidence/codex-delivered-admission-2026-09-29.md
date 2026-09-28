# Extracted Lite Codex admission qualification

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.

- Base dev: `38fbe92266bd4f675860e14c99aa7b971744cbd6`.
- Frozen test `1bacae3a9be00c77c648abe3c794bcd4df707109`, tree `3840de823617d3cd355e08d24f19385d3db7026d`: independent `/root/native_os_build_review` **REQUEST_CHANGES**. Its extracted fixture called `job inspect`, which did not prove effect-path refusal.
- Superseding test `8b0cba063b377ee8a03b4b87565c8a43840b0d6a`, tree `6e4c2075c70a86cc0b5061d88d9bce90b77418df`: independent `/root/native_os_build_review` **ACCEPT for dev test integration**. The exact delta calls extracted `job run`, asserts exit 1, structured `REFUSED`, precise local-model-permission reason and empty scratch; existing delivered Python job/wait/usage/context checks remain.

Command: `py -3 .aide/scripts/aide_lite.py job run --config .aide.local/execution.json --manifest .aide.local/efficiency-export-consumer-job.json`, under the approved shared D: runner with one intensive job. The saved local `-k` selector was stale and caused two zero-test runs (jobs `91d1e186c667491fad25c79a862b6cf9` and `ca3bb519f1df4214b3dc8bd9fd7757a5`); neither qualifies code. After correcting the local selector, the inspector version passed 1/1 in job `350c1327f9684e78afa503af6f85c0f3`, receipt SHA-256 `8dde3fb27e71e5a9161cd3bc3d2b352a42bc3a444ad50d54ea1041dd459a1cc6`, but review found the oracle gap.

The final run-path version passed 1/1 in job `dabd6ae65c7a435eae87c34b90f69bd4`, receipt SHA-256 `d70e1f8b659ca587c7ac6a94d74365174d09f2a46d9c485fc07e4d4d23b21f5e`. Its retained stderr ends `Ran 1 test ... OK`; the observation records peak memory 257,085,440 bytes, peak scratch 430 bytes, `scratch_absent=true`, `reservation_released=true`, and `model_requests_started_by_observer=0`. Retained receipt: `D:\Projects\AIDE\.aide.local\execution\retained\dabd6ae65c7a435eae87c34b90f69bd4\receipt.json`.

This is a disposable extracted pack from a test fixture, not the canonical stable release asset. No model turn was launched; the fake `codex.exe` is an admission fixture. Actual Codex JSONL completion, usage, effective context and final downloaded bytes remain unqualified.
