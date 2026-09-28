# First committed replay: expected metadata convergence

Clean artifact commit `4b5854f2f9dbeea7cf246946caf02d829a16c757`, tree
`a864e58a32a61f828248823c89f6f7cdc18e5033`, was replayed through six
serial D-managed commands: export-pack, changelog preview, release bundle,
release validate, release draft and release draft-validate. All child/runner
exits were zero, scratch retired and reservations released. The compact
external result list is
`D:\Projects\AIDE\.aide.local\execution\control\projection-replay-4b5854f2-results.jsonl`,
SHA-256 `1b95d430dadf79aea9398b1f665acd3d937a5c73c60ccda510198ed06d384d0c`.
Job IDs in command order:
`60727fcc26554542b62050768707c3d1`,
`aebf7ca2a432453ebcbd35897d2215f5`,
`bd7db1aa83e54efabe7ca1e9a550efe5`,
`5253438c15c141c5895eff06e53a3621`,
`243617788cb84907a9aa5d07cba6efec`,
`78cf27124da84c25b24f4a0f6d1a7e60`.

The replay changed **30 tracked derived files**, so its zero-change result
is **FAIL**, preserved explicitly. The export manifest's `source_commit`
advanced from `84e4a733...` to `4b5854f2...`; release/changelog/draft
metadata followed. ZIP and tar each retained the same 834 member names.
Comparing committed archive members with replay bytes found exactly one
changed content member in each: `aide-lite-pack-v0/manifest.yaml`. No source
payload member changed. Replay ZIP SHA-256:
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`;
tar.gz SHA-256:
`f0111bd834eb1aeb0b5b0ea70562ad7e1294c04dea8fa0bd83ab9be5cb294725`.
Current release provenance reports clean source `4b5854f2`, preview-only,
no-publish. Commit only this bounded metadata convergence and task evidence,
then replay from its new clean HEAD. Final zero-change replay and installed
consumer proof remain open.
