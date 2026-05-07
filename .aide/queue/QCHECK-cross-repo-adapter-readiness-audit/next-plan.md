# Next Plan

## Immediate Next 3

### 1. Q25 Importer Scope And State Truth Repair

Purpose:

- Update `.aide/profile.yaml` current focus and future intent after Q24/Q22/Q23.
- Update Harness self-check next-step guidance so it no longer recommends
  QFIX-02/Q21 after Q24.
- Add a target-scoped import mode or safe include/exclude policy.
- Regenerate the portable pack from a clean HEAD and make `pack-status` /
  `validate` pass, or explicitly record a reviewed pack provenance policy.

Acceptance:

- profile and self-check point to post-QCHECK next steps;
- direct importer can dry-run/apply a target-scoped import without copying broad
  optional `core/**`/docs surfaces unless requested;
- pack manifest source commit matches clean generation;
- `py -3 .aide/scripts/aide_lite.py pack-status` passes;
- `py -3 .aide/scripts/aide_lite.py validate` passes;
- no provider/model/network calls.

Non-goals:

- no Eureka product work;
- no Gateway/provider runtime;
- no adapter output expansion.

### 2. Q26 Eureka Pilot Review And Handover

Purpose:

- Review `EUREKA-AIDE-PILOT-01`.
- Accept/block/reconcile Eureka import evidence.
- Use `.aide/context/latest-task-packet.md` to select one bounded Eureka task.
- Seed Eureka-specific golden task candidates.

Acceptance:

- imported boundary verified;
- token report reviewed;
- next task has explicit scope, validation, evidence, and review gate;
- no product changes bundled into review.

### 3. Q27 Dominium Pilot Review And Doctrine Golden Tasks

Purpose:

- Review `DOMINIUM-AIDE-PILOT-01`.
- Confirm doctrine refs are sufficient and not inlined.
- Define Dominium-specific golden tasks for governance/schema/runtime-boundary
  work.

Acceptance:

- doctrine context report reviewed;
- task-specific curation gaps recorded;
- target golden-task seeds created or planned;
- no doctrine rewrite or product implementation bundled.

## Next 10

1. Q25 Importer Scope And State Truth Repair.
2. Q26 Eureka Pilot Review And Handover.
3. Q27 Dominium Pilot Review And Doctrine Golden Tasks.
4. Q28 Eureka Adapter Usage Pilot.
5. Q29 Dominium Adapter Usage Pilot.
6. Q30 Portable Pack Provenance And Release Candidate Checklist.
7. Q31 Target-Specific Quality Baseline Expansion.
8. Q32 Exact Tokenizer / Billing Measurement Spike.
9. Q33 Cache Usefulness Evidence Spike.
10. Q34 Gateway / Provider Readiness Audit.

## Decision Gates

- Do not perform broad target imports until Q25 resolves importer scope.
- Do not claim quality preservation for arbitrary coding until target-specific
  tasks and golden checks exist.
- Do not start Gateway/provider/runtime work until target handoff evidence is
  reviewed.
- Do not write preview-only adapter outputs to root/tool paths without managed
  section and drift policy review.
