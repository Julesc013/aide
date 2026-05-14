# Q37 Remaining Risks

- Deterministic heuristics only; there is no semantic LLM classifier,
  embedding search, or model-based repo understanding.
- Unknown files may need Q38 File Quality Ledger and Q39 Refactor Control Plane
  follow-up before any quality or structure decision.
- Orphan candidates are not deletion candidates.
- Dependency, test, and doc-link maps are conservative and can contain false
  positives or missed references.
- Source-generated repo intelligence reflects the current AIDE repository and
  must not be treated as target-repo truth.
- Target repositories must generate their own indexes after import.
- Q37 does not perform file quality scoring, root recycling, tool absorption,
  install/upgrade/rollback, target sync, branch mutation, or release work.
- Harness validation still reports pre-existing generated manifest drift and
  stale next-step wording from code outside Q37 allowed paths.
