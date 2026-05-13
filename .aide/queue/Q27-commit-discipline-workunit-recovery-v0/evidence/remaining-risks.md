# Q27 Remaining Risks

Status: COMPLETE FOR REVIEW.

## Remaining Risks

- Existing pre-Q27 commits remain malformed under the new standard. Q27 reports them but does not rewrite history.
- Local hook installation is opt-in. `core.hooksPath` is currently unset.
- Changelog preview is not release publishing and does not create tags, releases, or GitHub artifacts.
- Task recovery remains report-first and evidence-surface based. It does not prove task semantics or perform broad automatic repairs.
- Branch workflow policy and helper commands remain deferred to Q28/Q29.
- CI enforcement and GitHub branch protection remain deferred.
- The Harness still reports existing review-gate warnings for older queue items and a stale generated manifest source fingerprint. Updating `.aide/generated/manifest.yaml` is outside Q27 allowed paths and should be handled by a reviewed generated-artifact refresh.
- `scripts/aide self-check` still recommends Q25 review from the wider queue state. Q27 does not override earlier review gates.

## No New Blockers

- Q27 acceptance artifacts exist.
- AIDE Lite tests pass.
- Golden tasks pass.
- Export pack checksums pass.
- No live provider/model/network calls were introduced.
- No `.aide.local/`, `.env`, raw prompts, raw responses, or secrets were committed.
