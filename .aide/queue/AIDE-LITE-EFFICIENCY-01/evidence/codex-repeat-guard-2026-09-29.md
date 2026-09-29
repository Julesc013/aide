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

## Windows alias defect and superseding repair

Independent `/root/native_os_build_review` returned **REQUEST_CHANGES** for
frozen first source `d6581754faa2e59626daf5d12f378abacd8c3e7d`, tree
`bbc84d377bc192397f86cd580cbfc4d05d2e881c`. The raw fingerprint used
the spelling of `cwd`, `prompt_file`, `schema_file` and `inputs` keys; Windows
accepted case-only and trailing-separator aliases for the same files. That
allowed another turn under a two-turn local budget without new content.

The new case in `test_managed_workspace.py` exercises the same working root
under another case and separator, case-aliased prompt/schema keys, and a
duplicate aliased input. On first source, D job
`f0ca59ae15eb40efb9cb13062c2abb49` failed as expected because the
second request was admitted; manifest SHA-256
`bf261877f6ec26515c7f5b094d0c076e3af160e533d5c17d4da4b81b0d4c3428`,
receipt SHA-256
`7f33f9cbed98fa6977c3efb4b79c01c41c62bed088df944cc134037a5d2dbdb6`.
After the repair, D job `25adacce00ea444bb6ff956853eafede` passed the
one case; manifest SHA-256
`5fa768c056d81d6e9c7a878abd2d37c31cd6ce5b02892b7b422bc0a7d187be09`,
receipt SHA-256
`52674a88cfbb08367fbd953f6a92fab8fb310a4b4d9209660015d110063da08b`.
The job retired scratch and released its reservation.

The request fingerprint now uses the working-root filesystem identity,
source/tree, bound content hashes and explicit prompt/schema roles. Distinct
paths to one input file are rejected within a Codex job; no stable file ID
means refusal. The original 11/11 and 50/50 passes remain valid for the
first source only. The superseding source still needs full affected tests and
independent rereview, followed by changed-byte Lite qualification.

The superseding full managed-workspace command passed **51/51**, no skips,
in D job `46a3279f2b764476abc2ff2f7d2a0ac1`, exit zero, 69.458 seconds.
Its local manifest SHA-256 is
`0449299aa9a58c07f5978ed2437e44549f33736a2b1d78780b0c1b52aedd0a4c`;
retained receipt SHA-256 is
`aea7f1d31c501594b7581427cabc7850a38bc1d577722acec55b6314ad6f3a02`.
Peak Job memory was 239,575,040 bytes and scratch 33,124 bytes. The receipt
reports scratch absent and reservation released, and shared control has no
active job. Final tested source SHA-256 values are:

- `core/execution/managed_workspace.py`:
  `5dbe24b8294fed0ac02bc8e187ad3f4fc1c185bc375b4856204ac9428aa8a0d4`.
- `.aide/scripts/tests/test_managed_workspace.py`:
  `c0f0356cae735ca488390ce6740e7b675047dce6ad84a0eea61d0d91df2f7962`.

The test manifest also binds the unchanged CLI and Windows Job host hashes
listed above. No canonical pack or stable assets were rebuilt in this slice.

## Superseding independent source verdict

Reviewer `/root/native_os_build_review` returned **ACCEPT** for `dev` source
integration of exact superseding commit
`48235e9a43397e775102979214f0401dc3ccaaf7`, tree
`be0db1b9ad9212a691a6e15accd549c7e020e686`, against
`dev@ef0ecf1b6674ccf5ce0694398e37d66e4b3fdd95`. The reviewer
verified this evidence record's SHA-256
`538441e431e42575c154814dc477a8bebfa93a72223fdfb4c586d614cbd6029f`,
committed source/test hashes, a clean diff, and the retained red/green/full
receipts. The earlier case and trailing-separator bypass is closed by
filesystem identity for the working directory, content-bound inputs with
explicit prompt/schema roles, and refusal of duplicate file identities.
Durable dispatch history remains bounded and fail-closed before host launch.

The verdict applies to mediated `codex_exec` source integration. Live model
behavior, power-loss durability and delivered Lite release bytes remain
unqualified. It does not supersede the first candidate's REQUEST_CHANGES or
authorize model requests, main promotion, tags or publication.
