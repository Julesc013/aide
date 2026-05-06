# QFIX-02 AIDE Lite Test Discovery And Runner Fix ExecPlan

This is a living execution record for the bounded repair phase
`QFIX-02-aide-lite-test-discovery-runner`.

## Goal

Make AIDE Lite validation obvious and repeatable by diagnosing the broken
unittest discovery command, establishing a canonical AIDE Lite test command,
and updating tests/docs/evidence without changing product behavior.

## Scope

- Diagnose `.aide/scripts/tests` unittest discovery with and without `-t .`.
- Preserve `selftest` and add a clear `test` alias if it is the smallest robust
  command surface.
- Document the canonical command and the invalid/non-canonical old command.
- Add tests that protect importability, command behavior, and catalog guidance.
- Keep Q09-Q20 and QFIX-01 state truth intact.

## Non-Goals

- No Q21 export/import.
- No provider calls, model calls, Gateway forwarding, runtime behavior, UI, or
  autonomous execution.
- No broad packaging or module migration.
- No exact tokenizer, routing, cache, verifier, or golden-task feature changes.

## Validation Intent

Run Harness validation, AIDE Lite doctor/validate/selftest/test, both unittest
discovery forms, core Harness/Compatibility/Gateway/Provider tests, diff checks,
and a targeted secret scan. Record old-command behavior honestly.

## Progress

- 2026-05-07: Baseline validation started from a clean tree at
  `9adcfb0ca18a214d9955818839926185256d6392`.
