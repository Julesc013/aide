# Schema Review

PASS_WITH_WARNINGS. `.aide/protocol/aide-worker-run.schema.json` parses and is narrow to `kind: WorkerRun`, envelope fields, required metadata/spec/status fields, bounded provider/adapter/run-mode/status phase enums, and explicit non-capabilities. Warning: validation uses the accepted minimal local JSON Schema subset rather than full Draft 2020-12 enforcement.
