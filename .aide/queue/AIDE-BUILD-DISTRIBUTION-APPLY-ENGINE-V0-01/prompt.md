# Prompt: AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01

Create and process `AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01`.

Repo truth outranks this prompt. Build only. Stop at `needs_review`.

Goal: build DistributionApplyEngine v0 as a fixture-only, temp-workspace-only executor for accepted distribution update plan fixtures.

Authority:

- Add implementation, tests, fixtures, reports, queue packet, and evidence for DistributionApplyEngine v0.
- Mutate only copied temporary fixture workspaces during engine execution.
- Do not run independent check or acceptance.
- Do not mutate real target repositories or external repositories.
- Do not apply to the source repository.
- Do not create releases, tags, uploads, or GitHub Releases.
- Do not call provider/model/network services.
- Do not start self-consumer fixture, canaries, Workbench, Commander, Omnigent, live MCP mutation tools, live A2A delegation, source-change PreviewSession, DevelopmentTransaction apply, or PatchTransaction apply.

Required outputs:

- `core/distribution/apply_engine.py`
- `core/distribution/temp_workspace.py`
- `core/distribution/operation_executor.py`
- `core/distribution/rollback_verifier.py`
- `core/distribution/apply_reports.py`
- `distribution-apply status/plan/run/verify` CLI commands
- `.aide/fixtures/distribution-apply-engine-v0/**`
- `.aide/scripts/tests/test_aide_distribution_apply_engine_v0.py`
- `.aide/reports/distribution-apply-engine-v0/**`
- `.aide/queue/AIDE-BUILD-DISTRIBUTION-APPLY-ENGINE-V0-01/**`
- updated `.aide/queue/index.yaml`
- updated `PLANS.md` and `IMPLEMENT.md`

Expected result: `PASS_WITH_WARNINGS` with `material_finding_count: 0`, `missing_evidence: 0`, and recommended next task exactly `AIDE-CHECK-DISTRIBUTION-APPLY-ENGINE-V0-01`.

Stop at `needs_review`.
