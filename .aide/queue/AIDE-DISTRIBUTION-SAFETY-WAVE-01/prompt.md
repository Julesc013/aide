# Prompt: AIDE-DISTRIBUTION-SAFETY-WAVE-01

Create and process `AIDE-DISTRIBUTION-SAFETY-WAVE-01`.

Repo truth outranks this prompt. Inspect the live checkout before acting.

Goal: create the serialized Distribution Safety Wave plan that will build AIDE Lite install/update/rollback readiness through queue-governed build/check/accept/repair tasks.

Authority:

- Planning and queue materialization only.
- Do not implement InstallRecord or downstream objects.
- Do not perform install, update, migration, rollback, or uninstall apply.
- Do not mutate target repos, ScreenSave, Eureka, Dominium, or any external repository.
- Do not create release archives, tags, uploads, or GitHub Releases.
- Do not call provider/model/network services.
- Do not build runtime, Workbench, Commander, Omnigent, worker execution, PreviewSession, DevelopmentTransaction apply, or PatchTransaction apply.

Required outputs:

- wave task packet and evidence
- wave dependency map
- object responsibility map
- no-apply/no-publish boundary report
- validation matrix
- repair-routing matrix
- stop-condition matrix
- canary order rationale
- next concrete task prompt for `AIDE-BUILD-INSTALL-RECORD-V0-01`

Expected result: `PASS_WITH_WARNINGS`, `material_finding_count: 0`, `missing_evidence: 0`, next task `AIDE-BUILD-INSTALL-RECORD-V0-01`.

Stop at `needs_review`.
