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
