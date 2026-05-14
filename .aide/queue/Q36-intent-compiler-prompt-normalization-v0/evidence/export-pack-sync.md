# Q36 Export Pack Sync

Q36 updates `.aide/export/aide-lite-pack-v0/` so target repositories receive
portable intent compiler support without receiving source-local generated
latest intent packets or WorkUnit drafts.

## Exported Intent Files

- `.aide/policies/intent.yaml`
- `.aide/policies/workunit-sizing.yaml`
- `.aide/policies/task-classes.yaml`
- `.aide/policies/risk-classes.yaml`
- `.aide/policies/prompt-normalization.yaml`
- `.aide/intake/intent-packet.schema.json`
- `.aide/intake/workunit-draft.schema.json`
- `.aide/intake/intent-examples.yaml`
- `.aide/intake/README.md`
- `.aide/scripts/aide_lite.py`
- `.aide/scripts/tests/test_q36_intent_compiler.py`
- `.aide/evals/golden-tasks/intent_compile_vague_prompt_golden/**`
- `.aide/evals/golden-tasks/intent_compile_overbroad_prompt_golden/**`
- `.aide/evals/golden-tasks/intent_compile_destructive_prompt_golden/**`
- `.aide/evals/golden-tasks/intent_compile_git_prompt_golden/**`
- `.aide/evals/golden-tasks/intent_compile_install_prompt_golden/**`
- `.aide/evals/golden-tasks/workunit_sizing_policy_golden/**`
- `.aide/evals/golden-tasks/intent_packet_schema_golden/**`
- `.aide/evals/golden-tasks/catalog.yaml`
- `docs/reference/intent-compiler.md`
- `docs/reference/workunit-idempotency.md`
- `docs/reference/cross-repo-pack-export-import.md`

## Excluded Source-Local Outputs

- `.aide/intake/latest-intent-packet.json`
- `.aide/intake/latest-intent-packet.md`
- `.aide/intake/latest-workunit-draft.json`
- `.aide/intake/latest-workunit-draft.md`
- `.aide/evals/runs/**`
- `.aide/context/**`
- `.aide/github/**` generated reports
- `.aide/changelog/**` generated previews
- `.aide.local/**`
- raw prompts
- raw responses
- secrets and provider credentials

## Pack Status

`py -3 .aide/scripts/aide_lite.py export-pack --name aide-lite-pack-v0` passed
with 245 included files, 248 checksums, and boundary PASS.

`py -3 .aide/scripts/aide_lite.py pack-status` passed with checksums valid,
boundary PASS, and `DIRTY_SOURCE_RECORDED` provenance because the pack was
regenerated before the Q36 closure commit.
