# Delivered-byte mid-removal interruption qualification

Current source was clean `dev@2aaee82e96d275d83501785a073f6ba73c7b6594`, tree `9988836516a718e4507ceef693fa23bf6854c527`. The local 1.0.0 ZIP had SHA-256 `0d3ce38d1ab946d40590c8ead55c1ed1805ab12681258e84b792817ee6aec09d`, matching the release-effect manifest. The canary extracted its 835 safe members inside one disposable AIDE-managed D job, installed a brownfield project with authored `AGENTS.md` and a project-owned file, and obtained an exact removal plan.

The child process monkeypatched only its loaded delivered CLI to exit 77 immediately after the first successful receipt-owned file unlink (`.aide.local.example/README.md`). The parent observed that file absent, the removal intent and import receipt present, and the project-owned bytes intact. A fresh CLI process resumed `apply-removal` with the same plan digest and returned `DETACHED`. The final check found no receipt-owned files, removal state or runner; authored guidance and project-owned bytes were preserved. The [compact result](mid-removal-summary.json) records these observations. This is an actual child-process exit in a disposable consumer, beyond the earlier in-process `fail_after_removals` fixture.

Managed job `56478859dfd641a0a1481540fe58b303` exited 0, reached `retired`, released its reservation and removed its scratch. Peak memory was 255,680,512 bytes and peak scratch was 8,783,288 bytes. The retained receipt under the approved D retained root has SHA-256 `a62e57e3f6123c9544d5836c6d59be6af4aff9827903befe3aec9874a7fec4aa`. The retained result JSON has SHA-256 `52ccc6d3cdad7b40ded84801d9f56c8a34cdbb45fed6a66010d641876e94e730`; the Git-normalized LF copy is `f95eb8ee47df13a40ec0c5b0216137971e8b3250097e7435873313b8abd3bbaf`. The exact local job manifest and [canary source](mid-removal-canary.py) have SHA-256 `32d5f22d4eda6a9aea3a0e8750535233cc8412d82e004834d74407febd723b7f` and `2779ae46272031349881c035a28e52a5a4a6ed49914e68d717ff46afe616dec1` respectively; the existing lifecycle helper is `3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181`.

This verifies one Windows brownfield mid-removal boundary from local candidate bytes. It does not prove hostile concurrent mutation, every deletion point, another OS, a downloaded published asset, or release publication. The product source and frozen release ZIP were unchanged. Integrate this evidence only with an exact release-review delta or after the current frozen effect has completed its publication path.

Independent `/root/stable_effect_review` returned **ACCEPT for this additional
local evidence only** on `42832385`/tree `fa62b52d`. The actual verdict is
preserved in [mid-removal-review-42832385.md](mid-removal-review-42832385.md)
and externally under the approved D control root, SHA-256
`a7658862d70c4b4bf30e1876fba8c4fff7d9476fc9fb444ebba0a64f040deb31`.
The reviewer did not rerun the canary. Frozen release promotion still uses its
own exact head and historical-message gate.
