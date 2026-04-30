# Post-Q08 Cleanup Recommendations

## Stale `.aide/generated/manifest.yaml`

Classification: should fix before substantive next-horizon feature work.

Reason:

- The manifest source fingerprint is stale.
- `aide compile --dry-run` reports `.aide/generated/manifest.yaml: would_replace`.
- Generated artifacts are non-canonical, but drift should not become background noise.

Suggested QFIX:

- `QFIX-generated-artifact-refresh-v0`
- Run after status/catalog/docs cleanup so the manifest captures the latest source state.
- Use `aide compile --dry-run` first, then reviewed deterministic write only if the QFIX permits it.
- Record evidence and review the generated diff.

## Missing `aide self-check` Catalog Metadata

Classification: should fix before substantive next-horizon feature work.

Reason:

- `scripts/aide --help` exposes `self-check`.
- `docs/reference/harness-v0.md` and `docs/reference/self-hosting-automation.md` document it.
- `.aide/commands/catalog.yaml` does not list it.

Suggested QFIX:

- Add a bounded command catalog entry for `aide self-check`.
- Avoid broad Contract refactoring.
- Rerun Harness validation and generated-artifact dry-run.

## Q00-Q03/Q05/Q06 Raw Status Nuance

Classification: should fix before substantive next-horizon feature work, or explicitly document as a durable historical exception.

Reason:

- Q00-Q03 remain raw `needs_review`.
- Q05 and Q06 remain raw `needs_review` even though review evidence records `PASS_WITH_NOTES`.
- `aide-queue-next` and `aide-queue-run --no-prompt` point at Q06 because raw state is conservative.

Suggested QFIX:

- Preserve all historical queue packets and evidence.
- Add accepted review metadata or update statuses according to queue policy.
- Keep review-gated nuance visible in evidence.
- Do not delete or rewrite bootstrap-era records.

## Small Self-Check Proposed-Followup Wording Cleanup

Classification: should fix early next horizon.

Reason:

- Live `aide self-check` correctly reports Q08 as passed and recommends post-Q08 foundation review.
- Its `proposed_followups` list still includes: "Q08 review after this implementation stops at needs_review."
- This is stale wording, not an execution error.

Suggested QFIX:

- Narrowly adjust the self-check proposed-followup text to respond to Q08 raw/review status.
- Keep self-check report-first and non-autonomous.
- Do not add automatic worker invocation.

## Stale Root Documentation Phrasing

Classification: should fix early next horizon.

Reason:

- README and ROADMAP still contain phrasing that says Q08 review is next.
- PLANS has a current Q08 passed-with-notes entry, but one planned queue summary line still says Q08 is awaiting review.

Suggested QFIX:

- Perform a docs normalization pass limited to current state wording.
- Do not add new roadmap commitments.
- Keep future tracks marked candidate or deferred.

## Stored Self-Check Report Snapshot

Classification: acceptable deferred.

Reason:

- `.aide/runs/self-check/latest.md` is non-canonical evidence.
- It currently reflects the pre-Q08-review state.
- This review was not allowed to modify `.aide/runs/**`, so `--write-report` was not run.

Suggested QFIX:

- Optional: refresh the report in a reviewed report-only cleanup if useful.
- Do not treat the report as canonical queue state.
