# Handover Readiness

## Readiness Verdict

Ready for controlled Eureka import/handover pilot: yes.

Ready for serious Eureka product handover based on completed Q22 evidence: no.

The AIDE repo has a validated pack and adapter compiler, but the inspected
Eureka repo has not imported the Q21 pack. Handover must begin with import
reconciliation and measurement.

## What To Hand Over

- `.aide/export/aide-lite-pack-v0/`
- `install.md`
- `manifest.yaml`
- `checksums.json`
- import policy
- target-neutral memory/profile templates
- AIDE Lite script/tests
- adapter templates/previews
- docs/reference for export/import and adapter compiler

## What Not To Hand Over

- `.aide/queue/**` from AIDE
- AIDE project memory
- generated AIDE context
- AIDE reports, ledgers, cache keys, route decisions, gateway/provider status
- generated adapter previews as canonical root files
- `.aide.local/`
- `.env`
- secrets
- raw prompts or responses

## Eureka-Specific Preflight

The inspected Eureka repo already has `.aide/` contract files and does not
ignore `.aide.local/`. The first handover step must therefore be a dry-run, not
a blind copy.

Recommended command from a new Eureka branch:

```text
py -3 D:\Projects\AIDE\aide\.aide\scripts\aide_lite.py import-pack --pack D:\Projects\AIDE\aide\.aide\export\aide-lite-pack-v0 --target D:\Projects\Eureka\eureka --dry-run
```

Then:

1. Inspect conflicts with Eureka's existing `.aide/`.
2. Add `.aide.local/` to Eureka `.gitignore`.
3. Import only portable files that do not destroy existing Eureka contract truth.
4. Create Eureka-specific memory.
5. Generate snapshot/index/context/task packet inside Eureka.
6. Measure token reduction against a Eureka baseline.
7. Write Q22/Eureka evidence.

## First Real Eureka Task

Recommended first task:

```text
EUREKA-AIDE-PILOT-01 - Import AIDE Lite pack safely, reconcile existing Eureka .aide contract, generate compact task packet, and measure prompt reduction.
```

This is still an AIDE import pilot, not a Eureka product feature.

## Handover Blockers

- No Q22 target evidence yet.
- Existing Eureka `.aide/` may conflict with pack import.
- Eureka `.gitignore` does not yet ignore `.aide.local/`.
- Target-specific quality gates/golden tasks do not yet exist.

## Evidence Required To Clear Handover

- Eureka dry-run import report.
- Eureka import report.
- Eureka-specific memory files.
- Eureka latest task packet.
- Eureka token-savings report.
- Eureka quality/limitations report.
- Confirmation no AIDE source queue/memory/generated state was copied.
- Confirmation no secrets/local state/raw prompts/raw responses were committed.
