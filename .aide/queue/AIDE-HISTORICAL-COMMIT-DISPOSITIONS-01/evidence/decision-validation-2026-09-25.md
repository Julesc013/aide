# A/B/C decision binding and validation

The owner accepted A, B, and C in the current conversation on 2026-09-25
01:40:47 AEST. The agent transcribed the decisions into three structured JSON
artifacts and the source registry. `owner-decisions-2026-09-25.md` preserves
the provenance and narrow scope. No published commit object or message was
rewritten.

| Record | Commit | Tree | Message SHA-256 | Canonical record digest |
| --- | --- | --- | --- | --- |
| A | `bfb86c12b9e6d2970024d29c57ba629994ec43cc` | `54ab832eafa0ed0be3282858fd44f344e560732b` | `24d6d65e72424b7fca5dac30ebe638b2f7a16266d2c4e8e114dbb9bd6e0c380c` | `173b7e265767f95380164dcb0a6b4de09b4fa8e2c1b5d952d1ff1a0c8ca6b8b9` |
| B | `486e81cd3a918729f28e4b452a9dcff017238a04` | `796f5aafc0d350e8cef599cacb9b3f703f8b2bb1` | `71bcd1ba685a049c535e20244f65b29a1fef4299d4a0811f0c43031bd3b4dca0` | `e844704e33079c0e6b9f25939b03b2491c2713a7ac6384b78e19e52c73198199` |
| C | `1011d008fc39b135a5ef27062b5b8ee9c95cdc7f` | `68cbc4d2b15049b7c589204d29003cf4affd93fc` | `972e1349736a366c0a3b73189519c218bcb6b653fa8bb1a90bf73986034d3913` | `a1f061acb851359d37981549dab9c662da7565e8ff0412b9cb0709eeb693b403` |

The original registry already bound ordered parents, exact failed checks,
raw-failure evidence, and record digests. The decision update refreshed all
content hashes. Git objects were checked with replacement objects disabled
before writing. At 2026-09-25 08:36 AEST, the original UTC-only future-date
check rejected the owner's actual local decision date; a narrow date rule now
accepts a civil date once it has begun anywhere (UTC+14), while rejecting
dates that have not begun anywhere.

Local validation: 23 focused `test_q27_commit_recovery.py` cases passed;
three default exact `commit check --range <commit>^!` calls returned
`PASS_WITH_DISPOSITIONS` and showed the original 1/13/1 failures;
`git diff --check` passed. The independent reviewer also ran all three raw
`--no-dispositions` ranges, each of which still returned `FAIL` with those
same original counts. These are historical-message checks only.

Fresh independent technical delta review: Codex subagent
`/root/historical_date_review` (GPT-6 Sol), 2026-09-25,
**ACCEPT_WITH_NOTES** for the date repair and exact decision binding. It
confirmed the UTC boundary, hashes, 23 tests, default/raw range behavior, and
no review-time mutation. Its limitation is that it assumed the owner decision
in the conversation; it did not independently authenticate an owner timezone,
signature, product behavior, or release readiness. The earlier
`ACCEPT_WITH_NOTES` of mechanism source `59b886db` remains a separate review.

The branch's older generated release artifacts remain stale relative to dev.
Integrate eligible source and decision records against current dev, preserve
the accepted generator, then regenerate derived outputs from combined source.
