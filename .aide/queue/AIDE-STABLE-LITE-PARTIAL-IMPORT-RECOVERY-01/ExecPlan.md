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

- [x] Admit this bounded source task and preserve prior evidence effect.
- [x] Add failing partial-resume regressions and implement guarded behavior.
- [ ] Complete independent review, artifact projection and qualified dev effect.

The first red test raised `TypeError` for the absent explicit recovery option.
Focused Windows cases now pass for fresh and predecessor updates, a repeated
interruption, wrong identities and mode, changed controls, rival edits, linked
postimages, old intents, and changed manual resolution bytes. The full importer
suite was stopped on the rejected source; no passing result is claimed. Source review and
delivered-byte qualification remain pending.

Independent source review of frozen `547ea2b0` returned `REQUEST_CHANGES`:
forged, self-digested target intent could overwrite an authored file, and a
controls edit injected at receipt publication could produce a stale successful
receipt. The initial full importer run on that rejected subject was stopped;
it is not qualification for the repair. A superseding diff checks exact pack
operation coverage, action/ownership legality against the receipt/predecessor,
and controls/resolution inputs after receipt publication before retiring the
intent. Both reproduced defects and omitted-payload forgery now have passing
Windows regressions; full suite and independent rereview remain open.

Rereview rejected `052a0a92` because inputs could still change at intent
retirement. The next repair holds controls/resolution inputs through receipt
publication and intent deletion. An absent controls name is reserved with
CREATE_NEW and DELETE_ON_CLOSE; it cannot replace a project file and Windows
cleans it after abrupt process exit. Tests passed for a second-process writer,
process-exit cleanup, controls writes at both final boundaries, pinned manual
resolution at retirement, and the existing fresh/update recovery case. The
full suite on `052a0a92` was stopped; exact rereview precedes its replacement.
