# TestJob Schema Check

- task_id: AIDE-CHECK-TESTJOB-SCHEMA-01
- checked_task_id: AIDE-BUILD-TESTJOB-SCHEMA-01
- checked_commit: 017b7e639cd2fc48a5bfad8bf91e5665f0d56e9e
- result: PASS_WITH_WARNINGS
- selected_next_task: AIDE-ACCEPT-TESTJOB-SCHEMA-01
- attached_plan_next_after_acceptance: AIDE-BUILD-REFERENCE-ID-SCHEME-01

## Summary

No blocking defects were found in the minimal metadata-only TestJob schema slice. The schema, helper, projections, CLI dispatch, focused tests, predecessor compatibility checks, fail-closed command checks, secret scan, and overclaim scan passed.

## Warnings

- Full JSON Schema Draft 2020-12 validation remains deferred; the current validator uses the accepted minimal local subset.
- TestJob remains metadata-only and does not implement Test Broker runtime, async execution, scheduler, leases, worker execution, Service, Commander, providers, Gateway, network, GitHub mutation, branch automation, target apply, release, or promotion.
- `.aide/context/latest-task-packet.md` is stale relative to live queue truth.
- Initial PowerShell scan invocations were corrected and rerun.
- Generated report churn from validation was restored before artifact creation.

## Checked Behavior

- TestJob schema declares kind `TestJob` and public `apiVersion/kind/metadata/spec/status` shape.
- Compatibility, command, environment, framework, timeout, status, log, artifact, failure, retry, flake, evidence refs, and explicit non-capability metadata are present.
- `test-job status`, `test-job project --source accepted-artifacts`, and `test-job validate` pass.
- Unsupported `test-job submit/run/retry/summarize` subcommands fail closed.
- Nine projections are additive and report `source_reports_mutated: false`.
- Predecessor `worker-run`, `workunit-queue`, `evidence-packet`, and `contract-envelope` validations pass.

## Next

Proceed to `AIDE-ACCEPT-TESTJOB-SCHEMA-01`. After acceptance, the user-supplied frozen sequence points to `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.
