# Mediated Codex request repeat guard: source qualification

Date: 2026-09-29. WorkUnit: `AIDE-LITE-EFFICIENCY-01`. Candidate base:
`dev@ef0ecf1b6674ccf5ce0694398e37d66e4b3fdd95`, tree
`43cb3db231370a42c99e34d96457c64d4b929c23`. The changed source is
`core/execution/managed_workspace.py`; its focused oracle is
`.aide/scripts/tests/test_managed_workspace.py`. No live Codex process or
model request was launched by these synthetic-host tests.

| Stage | D job | Exact local manifest SHA-256 | Result | Retained receipt SHA-256 |
| --- | --- | --- | --- | --- |
| Red | `561fa2e902114515b2843326fe460a24` | `e5776a26fbfe288e8c42f8f7bc395695b963a817e1a3eecc29d7b395fc968fe1` | 1 expected failure: second unchanged request was admitted | `51680eb5bdfb4ff5231ec68377f5e7328edeeeef44436acdff0416559932d9df` |
| Focused green | `87e117166bd04659bf83320e0840fcc5` | `d016ba0e69472befc2ea37f05af6f627e8ad42708394960f1fdd37158684e002` | 11/11 PASS, no skips | `e8033f972592470454325bbadf30dadf74882f31dfcd75bb28089745899d2346` |
| Full managed workspace | `e0495c707b80499da54499d1fadc92a2` | `0e755994365bec147419b252fb29ec4bb737e50a4e3700fe7bddb69777e28d15` | 50/50 PASS, no skips | `0b7c3ffbbc6f34f0c3817ce52fc76ad88d4eec7a20ed8b143610126396581e3b` |

The red command selected
`test_codex_unchanged_request_refuses_before_second_allocation`; its retained
stderr says `WorkspaceRefused not raised`. Focused and full commands used
`python -m unittest discover -s .aide/scripts/tests -p test_managed_workspace.py`
with `-k codex -v` and `-v`, respectively. The full run took 46.847 seconds,
exited zero, peaked at 240,496,640 Job memory bytes and 8,783 scratch bytes.
The passing receipts report scratch absent and reservation released; shared
control had no active job afterward.

The full-run manifest bound these exact current input SHA-256 values:

- `core/execution/managed_workspace.py`:
  `12c1b239941d588c7615b856d987494b2d5bd29a322677aed8cf8037976a069d`.
- `.aide/scripts/tests/test_managed_workspace.py`:
  `510d5d7aa2c33e9ab85759a30db31e2f33628eb0a2991988d91c0f885ba5570a`.
- `.aide/scripts/aide_lite.py`:
  `e2b9890f51f26f14eb66551a7f0193fec02b725ba9582150637be6c4d5433986`.
- `core/runtime/continuous_worker/windows_job.py`:
  `77c0b404d7ea3383cd65c052999ed5265f97b97f4be8bc13ae35d7e49f8460fc`.

The guard covers the existing mediated `codex_exec` admission only. It
remembers a request before starting the host, so a crash or uncertain host
effect cannot cause silent identical replay. Prior positive-count dispatch
state without request identities refuses further Codex admission pending
reconciliation. It does not control internal or unmediated model requests,
qualify actual usage, or change the frozen 1.0.0 release bytes. Independent
source review and delivered-byte qualification remain open.
