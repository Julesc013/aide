# Independent API-set loader observation source review

Reviewer: `/root/native_os_build_review` (fresh independent subagent review, 2026-09-28)
Decision: **ACCEPT for source only**
Reviewed commit: `b682ba7d613836922970d675d5c7257a0205b8bc`
Tree: `1fa7e484963663cbbe12ab3517d3866bfd6a2844`
Parent: `3954ee4cbc725649269e675ef49ac3573f90f6a8`
Frozen source manifest SHA-256: `7c584552ee258b2372f780960e2926788bc0862f7f5d5af6cfdab94f5465bb28`

The reviewer checked the adapter's native signatures and search flag, exact-name and returned-path validation, refusal of truncated or foreign results, and `FreeLibrary` attempts for acquired handles. The six injected tests cover those paths. The reviewer verified the manifest's source, dependency, aggregate, and prior-manifest hashes and ran `git diff --check`. The reviewer observed the reported managed job result but did not rerun its suite or perform a native load.

Postcommit managed job `e04380a5b4fa48fa93c1efe881391006` on the reviewed commit/tree passed 59/59 affected injected tests, exit 0. Scratch retired and the reservation released. Retained receipt SHA-256: `558baaaf0959225fe65cf4b847365d33fa670f4402338d5c4bd0f0019ee73b48`.

**Effect limitation:** Windows loading may consult the loaded-module list, side-by-side state, and API-set mapping before the System32 directory search. `LOAD_LIBRARY_SEARCH_SYSTEM32` is therefore not proof that only System32 bytes execute. A path check happens after a load can execute DLL initialization or dependencies. This accepted source is observation only. An actual effect requires a separately reviewed exact manifest, controlled disposable child, durable intent, admission, and result analysis. It does not qualify host bytes, restricted loading, a worker, or release acceptance.
