# Next Task Prompt: AIDE-BUILD-INSTALL-RECORD-V0-01

Create and process `AIDE-BUILD-INSTALL-RECORD-V0-01`.

Repo truth outranks this prompt. Inspect live queue state before acting.

Goal:

Build InstallRecord v0 as a no-apply protocol/helper/projection/validation slice that records observed or completed AIDE distribution installation state without performing installation.

Authority:

- Implement InstallRecord v0 only.
- No install apply.
- No update apply.
- No migration apply.
- No rollback apply.
- No uninstall apply.
- No target repo mutation.
- No target scan authority beyond deterministic fixtures and existing project metadata authorized by the task.
- No release archives.
- No tags/uploads/GitHub Releases.
- No provider/model/network calls.
- No Workbench, Commander, Omnigent, worker execution, PreviewSession, DevelopmentTransaction, or PatchTransaction apply.

Read first:

- `.aide/queue/AIDE-DISTRIBUTION-SAFETY-WAVE-01/**`
- `.aide/reports/distribution-safety-wave-01/**`
- `.aide/reports/ownership-ledger-v1-acceptance/ownership-ledger-downstream-use.md`
- DistributionManifest schema/helper/tests/reports
- ProjectLock schema/helper/tests/reports
- OwnershipLedger schema/helper/tests/reports
- `.aide/queue/policy.yaml`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Implement:

- `.aide/protocol/aide-install-record-v0.schema.json`
- `core/protocol/install_record.py`
- `.aide/scripts/aide_lite.py` commands:
  - `install-record status`
  - `install-record project`
  - `install-record validate`
- fixtures under `.aide/fixtures/install-record-v0/**`
- tests under `.aide/scripts/tests/test_aide_install_record_v0.py`
- reports under `.aide/reports/install-record-v0/**`
- task-local evidence

InstallRecord v0 must model:

- `install_record_ref`
- `target_project_ref`
- `install_mode`
- `install_source`
- `source_distribution_ref`
- `project_lock_ref`
- `ownership_ledger_ref`
- `observed_existing_state`
- `installed_component_refs`
- `installed_file_entry_refs`
- `installed_managed_section_refs`
- `validation_refs`
- `evidence_refs`
- `warnings`
- `explicit_non_capabilities`
- `created_at`
- `created_by`
- `extensions`

Semantic validation must fail closed for:

- missing `source_distribution_ref`
- missing `project_lock_ref`
- missing `ownership_ledger_ref`
- source distribution mismatch
- project lock mismatch
- ownership ledger mismatch
- installed entry not present in OwnershipLedger
- managed section not present in OwnershipLedger
- install record claiming apply authority
- target mutation claims
- unknown required features
- absolute or traversal paths
- source output treated as target truth

Fixtures:

- valid fresh observed install
- valid existing observed install
- valid managed file observation
- valid managed section observation
- valid warning-only partial observation
- invalid missing distribution
- invalid missing lock
- invalid missing ownership ledger
- invalid source mismatch
- invalid ownership entry ref
- invalid apply claim
- invalid target mutation claim
- invalid unknown required feature
- optional extensions preservation

Validation:

- JSON schema parse
- compileall
- focused InstallRecord tests
- `install-record status`
- `install-record project`
- `install-record validate`
- DistributionManifest regression
- ProjectLock regression
- OwnershipLedger regression
- Q43-Q48 no-apply/no-publish validators
- broad `aide_lite.py validate`
- task inspect/evidence
- path, secret-like, and source-output misuse scans
- `git diff --check`
- `git diff --cached --check`
- `commit check --latest`

Stop at `needs_review`.

Recommend exactly:

```text
AIDE-CHECK-INSTALL-RECORD-V0-01
```
