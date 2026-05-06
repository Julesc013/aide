# Changed Files

## Queue And Evidence

- `.aide/queue/index.yaml` - added QFIX-02 and moved it to review state.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/task.yaml` - captured the bounded repair scope and final review status.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/status.yaml` - set QFIX-02 to `needs_review`.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/ExecPlan.md` - recorded diagnosis, implementation, validation, and review progress.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/prompt.md` - preserved the implementation prompt.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/changed-files.md` - this grouped file list.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/validation.md` - baseline, diagnosis, and final command results.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/test-discovery-diagnosis.md` - root-cause analysis for the hidden `.aide` discovery failure.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/test-runner-fix.md` - canonical test command and non-canonical command guidance.
- `.aide/queue/QFIX-02-aide-lite-test-discovery-runner/evidence/remaining-risks.md` - deferred work and no-call boundary risks.

## AIDE Lite Runner And Tests

- `.aide/scripts/aide_lite.py` - added the `test` command alias, kept `selftest`, and updated generated guidance to point at canonical validation.
- `.aide/scripts/tests/test_aide_lite.py` - added importability, command alias, controlled failure, and command-catalog coverage.
- `AGENTS.md` - refreshed the managed token-survival guidance section through `aide_lite.py adapt`.

## Harness And Command Truth

- `core/harness/commands.py` - updated post-foundation next-step guidance for the QFIX-02 review state and Q21 after acceptance.
- `core/harness/tests/test_aide_harness.py` - covered the active QFIX-02 guidance path.
- `.aide/commands/catalog.yaml` - added the implemented AIDE Lite `test` command and documented the non-canonical old unittest form.

## Documentation

- `README.md` - documented QFIX-02 and the canonical validation command.
- `ROADMAP.md` - updated the near-term repair sequence.
- `PLANS.md` - added the QFIX-02 plan and Q21 follow-on.
- `IMPLEMENT.md` - recorded the QFIX-02 implementation notes.
- `DOCUMENTATION.md` - indexed the new AIDE Lite test-runner reference and evidence.
- `docs/reference/aide-lite.md` - updated AIDE Lite validation guidance.
- `docs/reference/aide-lite-test-runner.md` - added the focused reference for canonical test execution.

## Deliberately Not Changed

- No provider, model, Gateway forwarding, Runtime, UI, Commander, cache, route, verifier, golden-task, or export/import behavior was added.
- No `.aide.local/`, secrets, raw prompts, raw responses, provider credentials, or local traces were created or committed.
