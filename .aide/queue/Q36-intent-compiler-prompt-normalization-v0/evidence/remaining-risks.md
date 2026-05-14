# Q36 Remaining Risks

- Classification is deterministic heuristic matching only; it is not semantic
  LLM understanding.
- Exact confidence is heuristic and intentionally conservative.
- Q37 Repo Intelligence Index v0 is needed for richer repo-local ownership,
  dependency, quality, and surface references.
- Q36 does not execute compiled WorkUnits. Queue intake, ExecPlans, evidence,
  validation, branch policy, and review gates remain required.
- Q36 does not mutate target repositories or sync Eureka/Dominium.
- Q36 does not publish releases, create tags, create GitHub releases, create
  `.github/workflows`, or apply GitHub branch protection.
- Q36 does not call providers, models, Gateway forwarding, GitHub APIs, or
  outbound network services.
- Harness validation still reports a generated-manifest source fingerprint
  warning. Refreshing `.aide/generated/manifest.yaml` is outside the Q36
  allowlist and should be handled by a reviewed generated-artifact refresh.
- Q36 commits were created on `main` because branch mutation was forbidden by
  the prompt and local policy prohibits ad hoc branch creation. This is recorded
  as a workflow risk, not as a branch-policy repair.
