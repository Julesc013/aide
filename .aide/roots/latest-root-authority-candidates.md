# Root Authority Candidates

- task_id: AIDE-STRUCTURE-00-current-truth-and-root-authority-audit
- generated_at: 2026-06-18
- source_commit: 53405366d5143ba540ad801352743d8472ff8288
- candidate_only: true
- no_apply: true
- file_moves: false
- file_deletes: false
- reference_rewrites: false
- new_roots_created: false
- root_contracts_created: false

## Candidate Authority Table

| Root | Observed status | Risk | Candidate authority |
| --- | --- | --- | --- |
| `.aide` | mixed | high | repo-local AIDE contract, queue, policies, evidence, reports, generated state, OKF projections, and control-plane status |
| `.aide.local.example` | review_required | high | template-only local runtime-state example |
| `.agents` | review_required | high | external agent/tool interop guidance and generated projections |
| `.codex` | review_required | high | Codex/tool interop projection only |
| `core` | mixed | high | reusable implementation library |
| `governance` | review_required | high | human-readable repository law and doctrine |
| `docs` | canonical | medium | human documentation, reference, operations, planning, decisions, and roadmap explanations |
| `inventory` | canonical | low | observed exact facts and records |
| `matrices` | canonical | low | cross-cutting support, capability, conformance, verification, host, bridge, risk, and release views |
| `hosts` | review_required | high | IDE and host integrations or host-lane proofs |
| `bridges` | canonical | low | target-repo bridge metadata and adoption expectations |
| `scripts` | canonical | low | stable command wrappers |
| `shared` | mixed | high | bootstrap-era shared implementation and tests pending fate mapping |
| `platforms` | review_required | high | candidate for split across hosts, environments, inventory, matrices, and docs |
| `research` | review_required | high | candidate human research input or compiled OKF/reference input |
| `specs` | canonical | low | bootstrap-era human and implementation-facing specifications pending authority split |
| `environments` | review_required | high | environment and execution-topology records |
| `evals` | review_required | high | evaluation definitions, runs, and golden checks |
| `fixtures` | canonical | low | canonical deterministic input and output fixtures |
| `packaging` | review_required | high | source packaging shape and release-bundle templates |
| `labs` | review_required | high | prototypes only |

## Add Only When Justified

- `tools`
- `tests`
- `examples`
- `archive`

This task did not create those roots. They should appear only after a reviewed
queue item proves current roots cannot express those authorities cleanly.

## Required Follow-Up

1. Root authority contracts.
2. Status and docs sync.
3. `shared`, `platforms`, `research`, and `specs` fate map.
4. Dot-tool roots interop policy for `.agents` and `.codex`.
5. `tools`, `tests`, `examples`, and `archive` root plan.
