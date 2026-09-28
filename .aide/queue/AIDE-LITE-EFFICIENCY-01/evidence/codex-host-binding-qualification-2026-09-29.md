# One-turn Codex host binding: source qualification

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`.

## Exact subject and review

- Base `dev`: `326492ff6df613ebb790111c9b80f7f0b94a790c`.
- Initial frozen review subject: `12ac93c9aeec68c38640082cbcd4541559c03a3d`, tree `2993918671eaf9e9f1ab66a007ff6557236fb521`.
- Independent `/root/native_os_build_review`: **REQUEST_CHANGES** on the initial subject. It identified missing local model permission/budget, underreserved retained stdin, and an unchecked executable parent chain. It did not qualify a live turn.
- Intermediate subject `33151c5ea97c05c2e9f10d5e91b96bf1f030ce46`, tree `cbc83880a98dcf2a8160517350ed0988ccb3b2ed`: independent **REQUEST_CHANGES** because the machine-local permission config still accepted duplicate JSON keys; it also noted a Python executable-path compatibility change.
- Final source subject: `67e1d572d513501b790abe92c60b6c2378198dfc`, tree `20393ddd96fb8e4fd3a2f61d01483223614a213d`.
- Final independent verdict: **ACCEPT for dev source integration** by `/root/native_os_build_review`, on exact `67e1d572`/`20393ddd`. The reviewer checked the prior blockers and final delta; `git diff --check` passed. This is a source verdict, not a live model or release verdict.
- Integration: `git plan` reported a task-branch dry run; `dev` was an ancestor, all eight `dev..HEAD` messages passed the commit range check, and the task worktree was clean. Local `dev` fast-forwarded to evidence closeout `6281a6b903ca5193aa6b8b9f15e1172ea4c04af1`. The observed remote `refs/heads/dev` then matched that full commit. No main/tag/release effect occurred.

The adapter extends `core/execution/managed_workspace.py` and the existing Windows Job host. It binds one prompt and result schema by source hash, uses explicit model and effort, and launches a read-only ephemeral Codex turn in owned scratch. A separate machine-local ChatGPT model/effort permission and finite admitted-turn count are required. Admission persists before launch; an uncertain launch consumes its slot. The dispatch lock is held across suspended-child resume. Prompt bytes count against the retained log limit, and the reservation includes collection overhead. Executable ancestors must be ordinary; the executable is hashed again just before process creation. Same-user malicious path mutation between final hash and process creation is outside this binding's guarantee.

## Deterministic qualification

Command: `py -3 .aide/scripts/aide_lite.py job run --config .aide.local/execution.json --manifest .aide.local/setup-focused-job.json`. This uses the existing approved D: managed roots and one resource-intensive job at a time. The manifest binds current source commit/tree, executable, fixture and test inputs. No model request was launched by these synthetic tests.

| Source | D job | Result | Retained receipt SHA-256 |
|---|---|---|---|
| `1105ad98` | `f1c8ecaafc274954928c149f0e7123b3` | FAIL 40/41: Windows active checkpoint sharing race | `08668a2449efc3d4eb86b287e95befca265b01415b62f562e75a66450064e104` |
| `12ac93c9` | `d988979a0272488da66940317c21d544` | PASS 42/42, then independent REQUEST_CHANGES | `ada9bac45fce7c7c3cdf9c1b96b070d3a5d6cd06cdb01274898f180e93041a29` |
| `36c94415` | `7421d4a494fb40b1b09dc3960d74f1d8` | FAIL 44/45: setup fixture used old reservation formula | `978723c6100c88dd66633b0db9cfad75fae6e0f7ee94eace2acb7b3050c655d4` |
| `33151c5e` | `7b43291cff56437eba4988c747bad325` | PASS 45/45, 36.479 seconds | `120f276472350e9b6949299d40630a8b5cca4acb1865023aafb9036f895707f3` |
| `67e1d572` | `5e5972bf8c444336b1a272721cc9f8dc` | PASS 46/46, 37.224 seconds | `78409b5b955a0130542c3025fa6815cae38c025d44ec4c593009824adc19e92a` |

The final job recorded peak memory 240,644,096 bytes and peak scratch 32,204 bytes. The result reports `scratch_absent=true`, `reservation_released=true`, and `receipt_present_outputs_unverified`; suite stderr ends with `Ran 46 tests ... OK`. The retention path is `D:\Projects\AIDE\.aide.local\execution\retained\5e5972bf8c444336b1a272721cc9f8dc\receipt.json`. No raw prompt, JSONL, or credentials are committed here.

## Remaining gates

- Extracted Lite qualification from current combined source after accepted integration.
- Actual Codex account permission, live turn/JSONL verdict and effective-context/usage evidence; a synthetic host exit does not prove a completed turn.
- Exact final release assets and promotion gate, separately.
