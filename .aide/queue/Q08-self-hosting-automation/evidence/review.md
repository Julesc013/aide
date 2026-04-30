# Q08 Self-Hosting Automation Review

## Executive Verdict

Q08 satisfies its ExecPlan and is safe to accept as the final item in the initial Q00-Q08 reboot sequence.

Review outcome: `PASS_WITH_NOTES`

The implementation keeps self-hosting automation report-first, local, deterministic, and non-autonomous. It adds `aide self-check`, a constrained `--write-report` path, clearer queue-runner reporting, and narrow doctor next-step cleanup without introducing Runtime, Service, Commander, external workers, provider/model calls, network calls, auto-merge, generated-artifact refresh, or post-Q08 implementation.

## Scope Review

Q08 stayed within the self-hosting automation scaffold described by the ExecPlan. The changed implementation surfaces are limited to Harness command wiring/reporting, conservative queue helper output, non-canonical self-check report evidence, docs, and Q08 queue evidence.

No forbidden post-Q08 foundation review files, Runtime/Host/Commander/Mobile/provider/browser/app/release surfaces, external CI, automatic Codex invocation, or autonomous service logic were added.

## Self-Check Behavior Review

`py -3 scripts/aide self-check` reports validation, queue health, review-gate nuance, generated manifest drift, Compatibility smoke posture, Dominium Bridge status, proposed follow-ups, and the next recommended step.

The report explicitly states:

- `mode: report-only`
- `mutation: none`
- `canonical: false`
- `external_calls: none`
- `provider_or_model_calls: none`
- `network_calls: none`
- `automatic_worker_invocation: false`
- `queue_auto_merge: false`

`py -3 scripts/aide self-check --write-report` writes only the deterministic non-canonical report path under `.aide/runs/self-check/`. The review run produced no git diff for `.aide/runs/self-check/latest.md` before review status edits.

## Queue Helper Review

`scripts/aide-queue-next` and `scripts/aide-queue-run` remain local, report-only helpers. They print queue status, task paths, prompt paths, and review-gate posture. They do not invoke Codex, call another external worker, mutate the repo, or bypass review gates.

`py -3 scripts/aide-queue-run --no-prompt` reports Q08 as the current review gate and clearly states `automatic_worker_invocation: false`, `mutation: none`, and `manual_start_required: true`.

After Q08 was marked passed, `aide-queue-next` and `aide-queue-run --no-prompt` fall back to older raw review-gated items, currently Q06, because Q00-Q03/Q05/Q06 status nuance is still unresolved. This is expected carry-forward status behavior, not a Q08 automation safety failure, because the helpers still refuse automatic invocation and expose review evidence nuance.

## Automation Permission Review

Q08 correctly draws the permission boundary:

- Allowed: inspect and report local repository state.
- Allowed only with explicit flag: write non-canonical self-check report evidence.
- Forbidden: external agents, providers, models, network services, auto-merge, release automation, generated artifact refresh, queue bypass, Runtime/Service/Commander behavior, and external CI.

Safety scans found no implementation path that performs external model/provider/network calls or automatic worker invocation. Matches for Codex, network, and auto-merge are negative boundary text, future target metadata, or test subprocess usage.

## Report/Evidence Model Review

`.aide/runs/self-check/latest.md` is clearly marked non-canonical and deterministic for the same repo state. It does not replace `.aide/`, `.aide/queue/`, generated manifests, Compatibility records, bridge records, or reviewed queue evidence.

After this review marks Q08 passed, the stored report remains an implementation evidence snapshot. Fresh command output from `aide self-check` should be used for current state in the post-Q08 foundation review; the report file should not be treated as canonical live state.

## Carry-Forward Issue Review

Q08 handled the carry-forward issues appropriately:

- Stale `.aide/generated/manifest.yaml` source fingerprint is reported and not refreshed.
- Stale doctor guidance that previously pointed at Q07 review is fixed; before review status edits, doctor correctly points at Q08 review.
- After review status edits, doctor correctly points at the post-Q08 foundation review.
- Q00-Q03 and Q05/Q06 raw review-gated status nuance remains visible and was not silently rewritten.
- `.aide/commands/catalog.yaml` still omits `aide self-check`; this is a metadata sync risk, not a blocker for post-Q08 foundation review.
- Live `aide self-check` correctly reflects Q08 as passed and recommends post-Q08 foundation review, but its static `proposed_followups` list still includes a Q08-review reminder. This is a should-fix cleanup before the next horizon, not a blocker, because the executable recommendation and queue health are correct and no mutation occurs.

## Source-Of-Truth Review

Source-of-truth boundaries remain intact:

- `.aide/` remains canonical for Profile/Contract records.
- `.aide/queue/` remains canonical for queue execution state.
- Generated artifacts remain non-canonical outputs.
- Self-check reports under `.aide/runs/**` are non-canonical evidence only.
- Q08 does not create a new source of truth outside the existing doctrine.

## No-Scope-Creep Review

No Runtime, Service, Commander, Host, Mobile, IDE extension, provider/model, browser, app, release, packaging, external CI, automatic agent invocation, queue auto-merge, or post-Q08 implementation was found.

No generated artifacts were silently refreshed. `.aide/generated/manifest.yaml` remains stale by source fingerprint and visible as a warning, as intended.

## Evidence Completeness Review

Required Q08 evidence exists:

- `.aide/queue/Q08-self-hosting-automation/evidence/changed-files.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/validation.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/automation-policy.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/self-check-output.md`
- `.aide/queue/Q08-self-hosting-automation/evidence/remaining-risks.md`

This review adds the required review evidence packet.

## Post-Q08 Readiness Implication

Post-Q08 foundation review may proceed. That review should treat Q08 as accepted with notes, rerun current self-check/validate/doctor output, and explicitly track the remaining cleanup items rather than relying on stale stored report snapshots.

## Final Review Outcome

`PASS_WITH_NOTES`
