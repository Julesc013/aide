# API-set query OS-build source repair

Scope: source and injected tests only, on branch
`task/aide-cw-api-query-effect-01` from `dev@2aaee82e96d275d83501785a073f6ba73c7b6594`.
The existing API-set query effect remains unprepared and unadmitted.

## Defect and change

The prior `NativeApiSetQueryApi.os_build()` read Python's
`sys.getwindowsversion().platform_version`. On this Windows host it returned
`10.0.19041`, while Python's OS `build` and WMI returned `10.0.19045`.
Python documents that `platform_version` derives from kernel32.dll and may
differ from the OS. `RtlGetVersion` is the documented Windows version API.
The adapter now binds that API, supplies the exact structure size, checks its
status, platform, major/minor and bounded build, and refuses invalid output.

Sources: https://docs.python.org/3/library/sys.html#sys.getwindowsversion ;
https://learn.microsoft.com/en-us/windows/win32/devnotes/rtlgetversion .

Changed source/test: `core/runtime/continuous_worker/windows_system_observation.py`,
`.aide/scripts/tests/test_continuous_worker_system_observation.py`.
Current exact source/dependency/test hashes are in
`h2-api-query-os-build-source-manifest.json` (SHA-256
`800fded315f7c78619df1724a37baf62c9042e31ae95207b86584f1b80b0e35e`).
The earlier reviewed source manifest remains unchanged.

## Validation

- `py -3 -B .aide/scripts/aide_lite.py job run --config .aide.local/execution.json --manifest .aide.local/native-os-build-job.json`: two new injected cases passed, exit 0; job `eb9e13549dae4ba7b8d6d967169e3fc5`.
- Same managed command with `native-os-build-suite-job.json`: 53 observation tests passed in 0.029s, exit 0; job `1ce2695643d04ebf80d729bab956e939`, peak memory 31,543,296 bytes.
- Same managed command with `native-os-build-probe-job.json`: read-only `RtlGetVersion` returned `10.0.19045`, matching `sys.getwindowsversion().build`; kernel32-derived value was `10.0.19041`; job `28ed5b32eb6440e3bcee777e5ea0ad3a`, peak memory 23,408,640 bytes.
- All three jobs retained bounded logs/results under the approved D retained root, retired scratch and released reservations. The local probe script and job manifests remain ignored local inputs. No API-set host query, profile, ACL change, network operation or worker activation occurred.

## Review and next effect gate

Independent exact-source review remains required before integration. The
actual 180-name native query additionally needs one frozen effect manifest,
protected write-ahead journal/controller, current OS/source/inventory pins,
managed deadline and independent effect review. Query output cannot qualify
private host bytes, loader isolation or operational activation by itself.
