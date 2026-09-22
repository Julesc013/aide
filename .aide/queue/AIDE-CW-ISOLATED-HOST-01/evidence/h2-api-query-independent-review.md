# H2 API-Set Query Independent Review

Verdict: **REQUEST_CHANGES** for commit
`ebf13af0dbef2dfbeab791dcb91eb8eb67a31c91` (tree
`e7c7ee2b9e5833ea78eedef2f0fbf44b784736e1`) over base
`c6fdc754844cf7d42302218ce08307a7e05dcb61`.

## Findings

### HIGH - the recorded 180-name closure cannot form a query plan

`core/runtime/continuous_worker/windows_python_contract.py:50` restricts API-set
names to `api-ms-win-*` or `ext-ms-win-*`, and
`core/runtime/continuous_worker/windows_system_observation.py:168` applies that
predicate to every query-plan name. The retained 180-name inventory includes
three valid `ext-ms-onecore-*` contracts at
`.aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h2-delay-system-readonly-final.json:2427`.
An independent construction of `ApiSetQueryPlan` from that exact inventory
failed with `Refused`; 177 names pass the predicate and these three fail:

- `ext-ms-onecore-appmodel-staterepository-cache-l1-1-0.dll`
- `ext-ms-onecore-appmodel-staterepository-internal-l1-1-1.dll`
- `ext-ms-onecore-appmodel-staterepository-internal-l1-1-4.dll`

The new tests at
`.aide/scripts/tests/test_continuous_worker_system_observation.py:467` and
`:476` use synthetic `api-ms-win-test-*` rows, so they prove the numeric limit
but not admission of the actual recorded workload. Microsoft documents the
contract grammar as an `api-` or `ext-` prefix followed by an alphanumeric/dash
body and a version suffix; it does not require `ms-win` in the body. Until the
predicate and exact-inventory regression are corrected, the claimed complete
180-name checkpoint is not implementable.

### MEDIUM - the 256-row change also widens the retained resource-map path

`core/runtime/continuous_worker/windows_python_contract.py:13` is shared by the
new query plan, `SystemContract`, and the historical `ObservationPlan` at
`core/runtime/continuous_worker/windows_system_observation.py:98`. That older
session calls `_mapping` once per admitted name at
`core/runtime/continuous_worker/windows_system_observation.py:446`. The changed
test at `.aide/scripts/tests/test_continuous_worker_system_observation.py:419`
now explicitly admits 256 names through that resource-mapping plan; an
independent 129-name probe also passed plan admission.

The 180-name evidence justifies a bounded 256-row ceiling for the system
contract and supported query path. It does not justify doubling the capacity of
the retained failed resource-mapping mechanism, particularly while the change
describes `NativeApiSetQueryApi` as separate from that path. Use separate
constants so the supported query/system contract can hold 180 names without
expanding the old mapping policy.

## Verified

- The reviewed commit has the requested base as its sole parent; all 16 changed
  paths are within the task allowlist.
- All four manifest file hashes match the exact clean checkout. The independently
  recomputed aggregate is
  `d6e30f285926acccbb3dd14cd0ec6672e966267a3131b37b177c7ae42449dda3`.
- The retained inventory contains exactly 180 distinct API-set names, so moving
  the relevant contract/query ceiling above 180 is numerically justified.
- The installed Microsoft SDK `apiquery2.h` declaration and the
  [Microsoft GetApiSetModuleBaseName reference](https://learn.microsoft.com/en-us/windows/win32/api/apiquery2/nf-apiquery2-getapisetmodulebasename)
  agree with the ctypes declaration: `PCSTR`, `UINT32` output-buffer capacity,
  `PWSTR`, optional `UINT32*`, `HRESULT`, and Windows calling convention. The
  source correctly checks `S_OK`, a returned length including the terminator,
  and a canonical bounded DLL basename.
- Session source consumes before dispatch, reserves before build/query calls,
  writes and verifies a per-name intent before each query, counts attempted
  backend calls before invocation, refuses partial output, and refuses replay
  on the same consumed session. Cross-process durability remains a protected
  journal premise for a later reviewed effect.
- The 256-name/257-call, 120-second, `MAX_PATH`, and 2 MiB bounds are explicit.
  Synchronous native-call interruption still requires the later effect's owned
  outer-process deadline.

## Validation

- PASS: exact branch, HEAD, parent, tree, clean-state, changed-path, and
  `git diff --check` inspection.
- PASS: four manifest hashes and canonical aggregate recomputation.
- PASS: 48 observation/query tests that do not instantiate
  `NativeApiSetQueryApi`.
- PASS: 64 Python-contract, Windows-image, Python-image, and PE regressions.
- PASS: 26 security source tests; the live loopback control was excluded.
- FAIL: exact retained 180-name `ApiSetQueryPlan` construction, with the three
  `ext-ms-onecore-*` refusals listed above.
- CONFIRMED: a 129-name historical `ObservationPlan` is now admitted, proving
  the unrelated resource-map capacity expansion.

The three tests that manufacture a `NativeApiSetQueryApi` instance with
`__new__` were not run because this review explicitly prohibited instantiating
that class. The socket-bearing security test was also not run. No native API
query, DLL load/map, file observation, profile, grant, AppContainer launch,
credential/provider access, network effect, Windows-state mutation, or Git
branch/push/merge/tag/release operation was performed.

This source review does not authorize or perform the actual native query or any
downstream effect. No real-host effect packet should be prepared from this
checkpoint until both findings are repaired and independently re-reviewed.
