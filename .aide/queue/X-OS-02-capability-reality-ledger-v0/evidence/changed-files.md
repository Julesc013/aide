# Changed Files

Changed scope:

- `.aide/queue/X-OS-02-capability-reality-ledger-v0/**`: queue packet, ExecPlan, prompt summary, status, and evidence.
- `.aide/capabilities/**`: capability seed records, README, observation schema, and overclaim schema.
- `.aide/policies/capability-reality.yaml`: X-OS-02 states, evidence classes, modifiers, overclaim classes, proof rules, and command boundary.
- `.aide/ledgers/capability-ledger.schema.json`, `.aide/ledgers/README.md`, and `.aide/examples/task-os/capability-ledger.example.json`: capability ledger schema/example updates and report-only boundary notes.
- `.aide/scripts/aide_lite.py`: capability parser group, report writers, validator, golden runners, export inclusion constants, and no-apply boundaries.
- `.aide/scripts/tests/test_x_os_02_capability_reality.py`: targeted parser, ledger, overclaim, validation, and golden-registration tests.
- `.aide/evals/golden-tasks/catalog.yaml` and six `capability_*` golden task directories.
- `.aide/reports/capability-*`: generated capability command status, observations, ledger, overclaim, and validation reports.
- `.aide/reports/task-os-*`: refreshed X-OS-01 report-only reports from full golden regression coverage.
- `.aide/evals/runs/latest-golden-tasks.*`: latest full golden task run, 158/158 PASS.
- `.aide/export/aide-lite-pack-v0/**`: refreshed portable pack with capability contracts, tests, docs, and golden tasks.
- `.aide/changelog/*preview*`, `.aide/changelog/latest-changelog-report.md`, `.aide/github/github-advisory.*`, `.aide/git/*plan.*`, `.aide/routing/latest-route-decision.*`, `.aide/context/latest-task-packet.md`, and `.aide/context/latest-review-packet.md`: generated validation, branch-safety advisory, next-task, and review evidence.
- `docs/reference/capability-reality-ledger.md`, `docs/reference/task-os-v0.md`, `docs/reference/task-os-report-only-commands.md`, and `docs/reference/README.md`: reference documentation and index sync.
- `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md`: planning, implementation, and documentation-state updates.

No target repositories, `.github/**`, provider/model credentials, release publication surfaces, Git branches, or target state were mutated.
