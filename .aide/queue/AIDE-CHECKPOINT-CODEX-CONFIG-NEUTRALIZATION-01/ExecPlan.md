# ExecPlan: Repository Codex Configuration Neutrality

## Objective

Keep repository-owned Codex files useful for role discovery without overriding
operator-selected model or execution settings.

## Scope

- Delete the repository-local `.codex/config.toml` pin surface.
- Reduce role TOML files to descriptions only.
- Document that session and user choices own execution settings.
- Record bounded queue evidence and a dedicated commit.

## Dependencies

- Approved `AIDE-CONVERGENCE-AND-DELIVERY-01` admission.
- Existing external recovery snapshot for the pre-checkpoint dirty state.

## Progress

- [x] Inspect repository and user configuration layers.
- [x] Remove repository execution-setting pins.
- [x] Preserve minimal role descriptions.
- [x] Complete bounded verification.
- [x] Commit the checkpoint; campaign publication follows with the closeout commit.

## Verification Intent

Scan active repository configuration, parse remaining TOML, run Codex strict
startup, and check the bounded diff for whitespace errors.

## Blockers

None for the completed checkpoint. Branch integration remains governed separately.
