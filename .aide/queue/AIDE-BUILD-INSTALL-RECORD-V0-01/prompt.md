# Prompt: AIDE-BUILD-INSTALL-RECORD-V0-01

Create and process `AIDE-BUILD-INSTALL-RECORD-V0-01`.

Repo truth outranks this prompt. Inspect live queue state before acting.

Goal: build InstallRecord v0 as a no-apply protocol/helper/projection/validation slice that records observed or completed AIDE distribution installation state without performing installation.

Required outputs include:

- `.aide/protocol/aide-install-record-v0.schema.json`
- `core/protocol/install_record.py`
- `install-record status`, `install-record project`, and `install-record validate` commands
- `.aide/fixtures/install-record-v0/**`
- `.aide/scripts/tests/test_aide_install_record_v0.py`
- `.aide/reports/install-record-v0/**`
- task-local evidence

Stop at `needs_review` and recommend exactly `AIDE-CHECK-INSTALL-RECORD-V0-01`.
