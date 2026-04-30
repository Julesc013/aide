# Q08 Automation Policy Evidence

## Implemented Automation Model

Q08 implements report-first self-hosting automation only.

Implemented command surface:

- `py -3 scripts/aide self-check`
- `py -3 scripts/aide self-check --write-report`
- improved read-only `scripts/aide-queue-next`
- improved read-only `scripts/aide-queue-run`

## Allowed Behavior

Q08 automation may:

- read local AIDE Profile/Contract, queue, generated artifact, Compatibility, Harness, and Dominium Bridge records;
- summarize validation, queue health, generated artifact drift, Compatibility smoke, and bridge posture;
- recommend follow-up QFIX or review work in report text;
- write `.aide/runs/self-check/latest.md` only when `--write-report` is explicitly provided.

## Forbidden Behavior Preserved

Q08 automation does not:

- invoke Codex, Claude, OpenHands, external workers, models, providers, browsers, network services, or external APIs;
- auto-merge, auto-commit, release, publish, package, or run CI;
- silently refresh generated artifacts;
- mutate `.aide/generated/manifest.yaml`;
- mutate Compatibility records, Dominium Bridge records, policy records, or external repositories;
- create executable queue task packets automatically;
- implement Runtime, Service, Commander, Hosts, Mobile, IDE extensions, app surfaces, release automation, or autonomous service logic.

## Report Output Policy

The explicit report path is `.aide/runs/self-check/latest.md`.

The report states:

- `canonical: false`;
- `mutation: none`;
- `external_calls: none`;
- `provider_or_model_calls: none`;
- `network_calls: none`;
- `automatic_worker_invocation: false`;
- `queue_auto_merge: false`;
- `generated_artifacts_refreshed: false`.

The report has no wall-clock timestamp and is non-canonical evidence, not source of truth.

## Carry-Forward Handling

- Stale `.aide/generated/manifest.yaml` source fingerprint: reported only; Q08 recommends a reviewed generated-artifact refresh QFIX.
- Stale doctor Q07 review guidance: fixed narrowly by computing the next recommendation from queue status.
- Q00-Q03/Q05/Q06 raw review-gate nuance: reported and not rewritten.
- Proposed task generation: not implemented; self-check recommends follow-up work in text only.
