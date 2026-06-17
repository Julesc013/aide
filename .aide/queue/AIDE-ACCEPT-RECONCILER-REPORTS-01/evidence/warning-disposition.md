# Warning Disposition

All warnings are non-blocking for `minimal_reconciler_reports`.

| Warning | Source | Blocking | Disposition | Reason | Future task |
| --- | --- | --- | --- | --- | --- |
| Reconciler is report-only and does not repair drift. | build, check, acceptance | false | accepted_with_warning | This is the intended capability boundary. | none |
| Findings are advisory and do not mutate queue/protocol/evidence/OKF truth. | build, check, acceptance | false | accepted_with_warning | Advisory findings are enough for this report-only slice. | none |
| Stale latest-task-packet drift remains open. | build, check, acceptance | false | accepted_with_warning | Queue truth remains canonical and context regeneration is not authorized here. | future context-pack or context refresh task |
| Acceptance gate debt remains open. | build, check, acceptance | false | accepted_with_warning | Queue review debt is reported, not repaired or superseded by Reconciler. | future review tasks |
| Stale OKF build report routing remains open. | build, check, acceptance | false | accepted_with_warning | Generated OKF build reports are historical outputs and are not source truth. | future authorized OKF refresh |
| OKF source-hash gaps remain open. | build, check, acceptance | false | accepted_with_warning | Hash gaps are detected and classified without refreshing OKF pages. | future authorized OKF refresh |
| Live finding schema differs from prompt field wording. | acceptance | false | accepted_with_warning | The live schema was validated by build and check; semantic non-repair and non-mutation fields are present. | future schema hardening only if desired |
| CapabilityManifest is not implemented. | build, check, acceptance | false | deferred | CapabilityManifest is the next task, not part of Reconciler acceptance. | AIDE-BUILD-CAPABILITY-MANIFEST-01 |
| ConformanceProfile, PatchTransaction, AdapterManifest, and ContextPack v2 are not implemented. | build, check, acceptance | false | deferred | These are later sequence items. | future queue tasks |
