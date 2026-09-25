# ExecPlan: AIDE-STABLE-LITE-PARTIAL-IMPORT-RECOVERY-01

## Objective and scope

Implement an explicit, exact-plan Windows reconciliation path for a portable
import that stopped after some payload writes. Current `dev@e88b1c2e` proved
real child-process safe refusal after the first payload, but cannot finish
that state. Keep the old intent format conservative; no silent replay, guessed
ownership, overwritten project bytes, or automatic feedback.

Allowed source is `.aide/scripts/aide_lite.py`, its focused importer tests,
the portable importer guide, this task and necessary parent/queue/plan records.
Generated pack and release outputs remain read-only until separate projection
after source review. No main, tag or publication effect is in this task.

## Plan

1. Admit this task from current `dev`, record the reviewed abrupt-exit evidence
   and observed dev effect. Freeze the source subject and archive identities.
2. Add red regressions for an explicit partial recovery request: fresh import,
   predecessor update, wrong pack/plan/predecessor, changed project controls or
   resolved bytes, unknown/backup states, repeated recovery, and competing
   target writes. Existing implicit retry must continue to refuse.
3. Persist the minimum full operation metadata in new intents. Verify the
   exact current/predecessor pack and target, digest-bound intent/plan, source
   bytes and project decisions before any resumed write. For each operation,
   accept only its exact preimage or postimage; use existing pinned Windows
   write machinery for remaining writes. Recheck every postimage and external
   control before receipt publication; retain intent on uncertainty.
4. Add an explicit CLI option with documented use and safe refusal for older
   or malformed intents. Run focused and adversarial tests, canonical checks
   and an extracted-archive process-exit consumer after current-source
   projection. Obtain independent technical source and artifact/effect review.
5. Integrate only reviewed source, then separately regenerate release-derived
   bytes from the accepted current generator. Keep remaining release gates
   explicit in the mandatory-profile matrix.

## Recovery

No forceful cleanup of a pending target intent. A failure or reviewer finding
stays recorded; repair the exact candidate and revalidate changed scope.
Cannot qualify with old local ZIP after source changes. The historical safe
refusal remains a valid fallback for old intents without replay metadata.

## Progress

- [ ] Admit this bounded source task and preserve prior evidence effect.
- [ ] Add failing partial-resume regressions and implement guarded behavior.
- [ ] Complete independent review, artifact projection and qualified dev effect.
