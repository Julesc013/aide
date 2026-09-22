# Independent Review Repair

## Findings Closed In Source

1. Git replacement objects are disabled for latest and range message reads as
   well as exact object facts. A disposable adversarial test installs a replace
   ref with a conforming message and proves raw range validation still reads
   and fails the original commit.
2. An accepted record requires a content-hashed structured JSON decision whose
   exact subject, decision, accountable identity, and date match the registry.
   The identity must be in the reviewed policy allowlist; dates before the
   policy window or after the current UTC date are refused.
3. Every registry entry is validated before any matching record can become
   effective. Non-object entries, malformed neighbors, duplicate disposition
   ids, duplicate exact commits, bad references, and bad record digests fail
   the entire registry closed.
4. The two new blank lines at EOF in `baseline.md` and `prompt.md` were removed;
   exact base-to-candidate `git diff --check` now passes.

## Retained Boundaries

- The three real dispositions remain `proposed` and ineffective.
- The decision request remains separate from any future structured decision.
- No history rewrite, force push, main promotion, tag, upload, publication,
  permission widening, or machine configuration change occurred.
- The repair needs a new portable pack generation and independent exact-commit
  rereview before integration.

## Portable Repair Candidate

- Source commit: `24a49c06ff84d4dbb83bfe608e9363be281b3869`.
- Bundle id: `aide-lite-pack-v0-24a49c06ff84d4db`.
- Export manifest SHA-256:
  `90466c461eb682fd870d96473d2ee4f84bbe62c6711903798407bd04bce723d6`.
- Export checksums SHA-256:
  `0bdec4b643db3dcd15714f694257671c1b9639d6bb4a827826c7e2b1d93959d5`.
- ZIP SHA-256:
  `ad2e50daf391ce760d24d45fbbdcf178b12f8685a925cb8a240100e4ddb20028`.
- tar.gz SHA-256:
  `01cabce16417175855f75f87fe4d6b1b25373007644be536b2b9bb114ea6b328`.
- Export payload, archive extraction, checksum, boundary, consumer, release,
  draft, canonical validation, and doctor checks pass.
- The local bundle and draft remain no-publish outputs.
