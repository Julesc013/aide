# Changed Files

## Queue Packet And Evidence

- `.aide/queue/Q44-repair-doctor-model-v0/**`: task packet, ExecPlan, review-gated status, and Q44 evidence.
- `.aide/queue/index.yaml`: Q44 queue entry.

## Policies And Schemas

- `.aide/policies/repair.yaml`
- `.aide/policies/repair-classes.yaml`
- `.aide/policies/repair-safety.yaml`
- `.aide/policies/repair-detection.yaml`
- `.aide/policies/repair-verification.yaml`
- `.aide/policies/doctor.yaml`
- `.aide/repair/*.schema.json`
- `.aide/repair/README.md`

## AIDE Lite

- `.aide/scripts/aide_lite.py`: added `repair observe`, `repair diagnose`, `repair plan`, `repair dry-run`, `repair validate`, `repair status`, `repair explain`, `repair classes`, and `repair doctor`; added repair golden-task hooks; exported Q44 portable files; kept repair operations no-apply.
- Fixed the repo-intelligence scan helper to read a bounded prefix of large text files so selftest dependency-map golden coverage remains deterministic after AIDE Lite growth.
- Narrowed secret-like path detection so docs, policies, tests, and golden tasks may mention secret-handling without being treated as committed secrets, while `.env`, `secrets/**`, credential, PEM, and key paths still block.

## Generated Repair Outputs

- `.aide/repair/latest-repair-observation.*`
- `.aide/repair/latest-repair-diagnosis.*`
- `.aide/repair/latest-repair-plan.*`
- `.aide/repair/latest-repair-dry-run.*`
- `.aide/repair/latest-doctor-repair-report.*`
- `.aide/repair/latest-repair-verification-plan.md`

## Tests And Golden Tasks

- `.aide/scripts/tests/test_q44_repair_doctor.py`
- `.aide/evals/golden-tasks/repair_*_golden/**`
- `.aide/evals/golden-tasks/catalog.yaml`

## Documentation

- `docs/reference/aide-repair-model.md`
- `docs/reference/aide-install-model.md`
- `docs/reference/cross-repo-pack-export-import.md`
- Root docs updated earlier in Q44: `README.md`, `ROADMAP.md`, `PLANS.md`, `IMPLEMENT.md`, `DOCUMENTATION.md`, and `AGENTS.md`.

## Export Pack And Next Packet

- `.aide/export/aide-lite-pack-v0/**`: regenerated with Q44 repair policies, schemas, docs, tests, golden tasks, and updated AIDE Lite script. Source-generated `.aide/repair/latest-*` outputs are not exported as target truth.
- `.aide/context/latest-task-packet.md`: regenerated for Q45 Upgrade Model v0.
