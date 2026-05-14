# Q38 Remaining Risks

## Remaining Risks

- Q38 uses deterministic heuristics only. It does not perform semantic LLM
  quality scoring.
- Unknown kind, owner, and status warnings remain for future Q38/Q39 review;
  they are not treated as product failures.
- Orphan candidates are not deletion candidates. They mean "inspect before
  acting."
- Stale doc path candidates can include examples, historical references, and
  intentionally unresolved placeholders.
- Test and validator mapping is conservative and does not prove runtime
  coverage.
- Reuse/modularity candidates do not prove duplication or justify extraction.
- Gateway validation passes but remains slow because its suite invokes broad
  AIDE Lite checks.
- Target repositories must generate their own repo intelligence and quality
  ledgers; AIDE source reports are not target truth.
- Q39 Refactor Control Plane v0 and Q40 Root Recycling Framework v0 are needed
  before any refactor, movement, or deletion action can be considered.
