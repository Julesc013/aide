# Prompt

Task ID: `AIDE-LIFECYCLE-FIXTURE-INSTALL-DRY-RUN-01`

Run no-apply, report-only/dry-run install planning checks against generated install lifecycle fixture plans. Review install scenarios only: `install-clean`, `install-existing-manual-preserved`, `install-managed-section`, `protected-path-blocked`, and `traversal-blocked`. Compare generated plans with fixture metadata, generated plan reports, expected install reports where present, expected states, allowed/protected paths, managed-section expectations, hash references, no-mutation flags, scoped executor v0 limitations, and capability labels. Produce deterministic reports and task-local evidence. Do not implement or execute install apply, lifecycle apply, scoped transaction fixture apply, active repo apply, target repo mutation, branch/worktree mutation, release, GitHub, provider/model, Gateway, network, promotion, or broad active-repo apply. Stop at `needs_review`.
