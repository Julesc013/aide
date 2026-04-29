# Q03 Validation

Validation was run on 2026-04-29 for the Q03 Profile/Contract v0 implementation.

## Commands And Results

| Command | Result |
| --- | --- |
| Required file and directory `Test-Path` checks for `.aide/profile.yaml`, `.aide/toolchain.lock`, `.aide/components/`, `.aide/commands/`, `.aide/policies/`, `.aide/tasks/`, `.aide/evals/`, `.aide/adapters/`, `.aide/compat/`, `core/contract/`, `docs/reference/profile-contract-v0.md`, and `docs/reference/source-of-truth.md` | Passed. All required paths exist. |
| Required component-id scan for `core-contract`, `core-harness`, `core-compat`, `core-control`, `core-runtime-deferred`, `core-sdk-deferred`, `hosts-deferred`, `bridges-dominium`, `docs`, and `queue` in `.aide/components/catalog.yaml` | Passed. All required component ids are declared. |
| Command catalog scan for queue helper commands, future `aide` commands, `queue-helper-script`, `future-harness-command`, `implemented`, and `planned` | Passed. Implemented queue scripts and planned Harness commands are distinguished. |
| `git diff -- .aide/policies/autonomy.yaml .aide/policies/bypass.yaml .aide/policies/review-gates.yaml` | Passed. Existing autonomy, bypass, and review-gate policy files are unchanged. |
| `Select-String` for `Profile` and `Harness` in `core/contract/README.md`, `docs/reference/profile-contract-v0.md`, and `docs/reference/source-of-truth.md` | Passed. The docs explain Profile versus Harness. |
| `py -3 scripts/aide-queue-status` | Passed. During implementation Q03 reported `running`; after final status update Q03 reports `needs_review`. |
| `py -3 scripts/aide-queue-next` | Passed. During implementation and after final status update, the next pending item is `Q04-harness-v0`. |
| Python standard-library YAML-like sanity check for tabs and `schema_version` markers across new `.aide/` YAML records and queue records | Passed. Checked 18 YAML-like files. |
| Python standard-library Markdown sanity check for top-level headings and tabs across new contract/reference docs and evidence | Passed. Checked 17 Markdown files. |
| Terminology scan for `Profile`, `Harness`, `source of truth`, `generated`, `toolchain.lock`, `Contract`, `Compatibility`, `Dominium Bridge`, `self-hosting`, and `pre-product` | Passed. Required terms appear in expected contract/root docs. |
| `git diff --check` | Passed with line-ending normalization warnings only. No whitespace errors were reported. |
| Allowed-path audit over changed and untracked files | Passed. All changes are inside Q03 allowed paths. |

## Heavy Tests

No heavy native host tests were run. Q03 is a documentation and declarative contract task, not a host, Runtime, Harness, or provider implementation task.

## Result

Q03 validation passed for the minimal Profile/Contract v0 implementation. Q03 stops at `needs_review`.
