# Remaining Risks

## Risks

- Q40 is dry-run only. It does not implement root moves, file moves, deletes,
  path aliases, shims, salvage maps, or reference rewrites.
- Root status, risk, and fate classification are deterministic heuristics. They
  reduce ambiguity but do not prove semantic ownership.
- Unknown-owner and high-risk roots require human or future WorkUnit review.
- Orphan, unknown, mixed, and review-required signals are not deletion
  candidates.
- Target repositories must generate their own root inventories and plans after
  import; AIDE-local generated root outputs are not target truth.
- Q41 Existing Tool Absorption v0 is needed before root recycling can classify
  existing target-local tools such as XStack/AuditX-style surfaces.
- Q42 and later move/salvage/path-alias phases are required before any reviewed
  apply-capable root migration can exist.
- Local `main` remains ahead of and behind `origin/main`; Q40 did not merge,
  push, prune, delete, or create branches.
