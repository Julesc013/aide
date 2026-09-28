# Delivered task inspection CLI, 2026-09-28

The current local preview ZIP SHA-256
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`
was used in three bounded D jobs under source
`b94d7ba940e2455f69f96ba345013e19ba7c7645`, tree
`924e2fbf6387ed32f29adc236fae24e0819180e9`.

The first task-form trial `ee5b4443f0e3475985dc1b7082ea501f` returned
child exit one because the canary wrongly expected a fresh target with no
queued tasks to return success from `task status`. Its scratch and reservation
were retired; the failed oracle did not retain that command's diagnostic.
The corrected diagnostic job `3e57b229664a43b491a574bfe560f5bc` retained
the exact output: an empty target reports `task_count: 0`, and `task inspect`
reports `classification: missing`; both exit one and do not mutate the
target. This matches the source command contract, not a product defect.

The final delivered-byte job `13be19eb20344b12aa667204723af145`
extracted 834 ZIP members and installed into a disposable target. It verified
the same empty-state exits and no mutation, then created one project-owned
running queue task. Installed `task status` and `task inspect --task-id
LOCAL-PUBLIC-CLI-CANARY-01` both exited zero; inspection returned
`classification: partial` and `continue_from_status_and_evidence`. A before
and after target tree comparison showed no inspection mutation. The earlier
feedback/explanation checks also passed in this final job: default no packet,
explicit local manual-only packet, unknown rationale, and refusal without
dry run. Child exit zero; peak scratch 8,187,878 bytes, peak memory
227,274,752 bytes, scratch retired and reservation released.

Final oracle SHA-256
`bc4beb41ffc68d4f7d4c8b04975f8b2d39a9cf82f39f4c79525e076d060d19de`;
manifest SHA-256
`987173b5807beb59d5833eb13b05df30368e40cefab7dffaf6d176e8b67a513c`;
summary SHA-256
`c1681fca3109e5fd8ec777e34d15bf10fa551c66cbc253dac6be91ad58da6710`;
retained receipt SHA-256
`d0b2c9a113ae82aae81241b31d843ca3bd7a5ffaa6792c363c86cac154136a89`.
This is local preview evidence, not final downloaded-byte acceptance.
