# Next Plan

## Immediate Fixes Before Continuing

1. Do not treat Q22/Q23 as completed.
2. Update future handover prompts to acknowledge local Eureka already has an
   older `.aide/` contract and needs conflict-aware import.
3. Fix residual `scripts/aide self-check` next-step guidance after Q24 in a
   small state-truth cleanup if it continues to confuse agents.

## Next 3 Queue Items

### 1. Q22-RUN Eureka AIDE Lite Import Handover Pilot

Run in `julesc013/eureka`, not AIDE.

Prompt must include:

- preserve existing Eureka `.aide/` content;
- dry-run import first;
- add `.aide.local/` ignore;
- create Eureka-specific memory;
- generate snapshot/index/context/task packet;
- measure prompt reduction;
- write import/token/quality evidence;
- no Eureka product changes.

Acceptance:

- Eureka `.aide/context/latest-task-packet.md` exists;
- token-savings report exists;
- no AIDE queue/history/memory/generated state copied;
- no secrets/local state committed.

### 2. Q23-RUN Dominium AIDE Lite Import Pilot

Run in `julesc013/dominium`, after preserving unrelated dirty files.

Prompt must include:

- doctrine refs by path, not doctrine dumps;
- compact Dominium memory;
- snapshot/index/context/task packet;
- doctrine-context report;
- token-savings report;
- no product/governance rewrites.

Acceptance:

- Dominium `.aide/context/latest-task-packet.md` exists;
- doctrine-context report exists;
- no source AIDE state copied;
- no secrets/local state committed.

### 3. Q25 Target-Pilot Adapter Guidance Review

Run in AIDE after target pilot evidence exists.

Prompt must include:

- compare adapter previews with target pilot friction;
- trim verbose or unused guidance;
- decide if any preview target should become managed in imported repos;
- keep generated outputs non-canonical;
- no IDE/runtime/provider work.

Acceptance:

- adapter guidance refined from real pilot evidence;
- manual content preservation still tested;
- export pack updated only for templates/policy.

## Longer Queue

1. Eureka import pilot.
2. Eureka import review and first compact implementation task.
3. Dominium import pilot.
4. Dominium doctrine-context review.
5. Adapter guidance pilot refinement.
6. Target-specific golden tasks for Eureka.
7. Target-specific golden tasks for Dominium.
8. Cross-repo pack v0.1 from pilot lessons.
9. Post-pilot checkpoint audit.
10. Gateway/provider policy review only after target token/quality evidence.

## Explicit Non-Goals

- No Gateway forwarding.
- No provider/model calls.
- No target product feature work during import pilots.
- No autonomous loops.
- No IDE extension implementation.
- No exact tokenizer/provider billing until after target-pilot value is proven.

## Decision Gates

- Handover gate: target import proof and token-savings report.
- Quality gate: target-specific verifier/golden/evidence checks.
- Adapter write gate: target-specific manual content preservation and drift
  evidence.
- Provider/Gateway gate: reviewed policy plus target-quality evidence, not just
  local skeleton readiness.
