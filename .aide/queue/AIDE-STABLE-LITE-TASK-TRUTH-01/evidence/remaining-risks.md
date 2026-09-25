# Remaining risks, 2026-09-25

- Source tests do not prove the fix is present in the delivered archive. A
  separate projection must regenerate from the current accepted generator,
  qualify post-commit replay, and rerun the clean installed-target command.
- `task status` still exits 1 with zero queue items by existing convention.
  This source task deliberately does not change that contract.
- Target queues with nonempty project-owned items need separate behavior
  qualification. This candidate only repairs the observed empty-queue report.
- Technical review, dev integration and all final stable release gates remain
  open. No source acceptance or release readiness is inferred from this file.
