# Next Horizon Plan Recommendation

## Decision

The next horizon may begin, but it should begin with cleanup and reconciliation before new feature implementation.

Recommended decision:

- close Horizon 1 as complete with cleanup notes;
- run a bounded QFIX cleanup pair;
- then open Q09 or an equivalent next-horizon planning packet.

## Proposed Next Task IDs

1. `QFIX-h1-status-catalog-doc-cleanup`
   - Purpose: reconcile accepted queue status nuance, add missing `aide self-check` command catalog metadata, clean stale self-check proposed-followup text, and normalize stale README/ROADMAP/PLANS phrasing.
   - Type: cleanup, not new architecture.
   - Review gate: required.

2. `QFIX-generated-artifact-refresh-v0`
   - Purpose: run the reviewed deterministic generated-artifact refresh after the cleanup changes alter generated source fingerprints.
   - Type: generated artifact maintenance.
   - Review gate: required.

3. `Q09-next-horizon-planning`
   - Purpose: choose and plan the next substantive horizon after cleanup.
   - Type: planning only.
   - Review gate: required.

## Cleanup Before New Feature Work

Cleanup is recommended before new feature work because the current warnings are not dangerous, but they will create confusion for future automation:

- queue helpers point at old raw review gates;
- generated manifest drift is expected but noisy;
- Contract command metadata does not list `aide self-check`;
- root docs still point at Q08 review as next work.

## Recommended First Next-Horizon Track

The first track should be "foundation hygiene and next-horizon selection":

- reconcile queue status/review evidence;
- refresh command catalog metadata;
- normalize root docs;
- refresh generated artifacts through the Q05-reviewed path;
- then decide the first substantive new track.

## Candidate Substantive Tracks After Cleanup

These are candidates, not commitments:

- planning for a small Pack/Skill/Workflow IR vocabulary;
- planning for deeper Harness schema validation;
- planning for host-lane evidence refresh;
- planning for Runtime boundaries without implementing Runtime;
- planning for Dominium adoption workflow without touching the Dominium repo.

## Deferred Tracks

- Runtime implementation
- Hosts implementation expansion
- Commander
- Mobile
- IDE extensions
- provider/model/runtime adapters
- browser bridges
- app surfaces
- release/package automation
- external CI
- automatic Codex or external worker invocation
- autonomous service behavior

## Do Not Start Yet

Do not start these until a reviewed plan explicitly authorizes them:

- Pack/Skill/Workflow IR implementation
- Runtime or Service implementation
- Host/App/IDE extension work
- Dominium repo mutation
- generated Dominium outputs
- provider/model/network integrations
- automatic queue execution or auto-merge behavior

## Recommended Planning Prompt

Use a next prompt that first asks for `QFIX-h1-status-catalog-doc-cleanup`, not a new feature:

> Create the plan for `QFIX-h1-status-catalog-doc-cleanup` to reconcile post-Q08 queue status nuance, add missing `aide self-check` command catalog metadata, clean stale self-check follow-up wording, and normalize stale root docs. Do not refresh generated artifacts in that task; plan a separate reviewed generated-artifact refresh afterward.
