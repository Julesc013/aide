# Capability Boundary

Authorized:

- exactly one local read-only fixture-backed invocation of
  `dominium.validation.run`;
- deterministic fixture reads under
  `.aide/fixtures/dominium-workunit-validation-slice/workspace`;
- deterministic report and projection writes under
  `.aide/reports/dominium-workunit-validation-slice`.

Forbidden and observed false:

- arbitrary shell command execution;
- private tool call;
- broad Dominium command dispatch;
- provider/model/network call;
- worker execution;
- Workbench apply;
- preview/apply behavior;
- PatchTransaction apply;
- source or target repository mutation;
- branch or worktree creation;
- GitHub mutation;
- release or promotion.

The generated validation report requires the false-boundary fields to remain
false and requires the invocation count to remain exactly one.
