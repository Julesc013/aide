# ExecPlan: Delivered Pack Import Closure

## Objective

Produce release archives whose extracted bytes form a complete, internally
consistent AIDE Lite pack and can drive safe import into a fresh disposable
repository without the development checkout.

## Scope

- Replace the shape-only release fixture with an executable consumer oracle.
- Preserve forbidden-path filtering while reconciling manifest and checksum
  identities with the archive's actual payload.
- Validate ZIP and tar.gz extraction, isolated CLI execution, dry-run, safe
  import, target-local execution, and deterministic rebuilding.
- Regenerate only the owned export and local release artifacts after code and
  tests pass.

## Dependencies

- `dev@d37219026462d5670f7a724980faf07e30abb85f`.
- Existing Q47 exporter, release builder, importer, and safe-write machinery.
- Owner-admitted `AIDE-CONVERGENCE-AND-DELIVERY-01` campaign.
- External mission pack verified separately; it supplies direction, not repo law.

## Write Ownership

- This task owns the release projection implementation and Q47 regression file.
- This worktree exclusively owns its queue record, latest intake projection,
  regenerated release artifacts, and task-branch Git metadata during the slice.
- Broker, host, target-qualification, `.codex`, and GitHub configuration remain
  owned by their existing streams.

## Progress

- [x] Refresh exact refs and create an isolated task worktree from current dev.
- [x] Compile the aggregate request and preserve its split-required result.
- [x] Reproduce the extracted archive checksum failure outside the checkout.
- [x] Add and run an executable regression that fails on the current builder.
- [x] Implement a deterministic archive projection with truthful metadata.
- [x] Run focused and adjacent validation against extracted ZIP and tar.gz bytes.
- [ ] Regenerate and validate owned local artifacts.
- [ ] Record evidence, commit explicit paths, and publish the task branch.
- [ ] Prepare and evaluate the exact task-to-dev integration candidate.

## Test Oracle

The regression must invoke the script stored inside each extracted archive with
isolated Python, use that extracted directory as `--pack`, and target a newly
initialized disposable Git repository. A pass requires checksum validation,
dry-run success, safe import success, an installed target CLI, no forbidden
archive or metadata paths, and equal bytes across repeated archive builds.

## Recovery

The branch is based directly on published `dev`; no broker history is included.
Before integration, abandon only this worktree and branch if the candidate is
invalid. After publication or integration, recover through a reviewed revert;
never rewrite shared history or force-push.

## Implementation Checkpoint

The baseline consumer test failed for both archive formats because the filtered
secret-placeholder path remained in `checksums.json`. The implementation now
constructs a temporary permitted-payload projection, regenerates its manifest,
checksums, and export report, validates that projection, and archives only those
bytes. Q47, export/import, governance-export, release-draft, self-consumer, and
product-status tests pass. A release generated from the dirty implementation
tree also completed a fresh-repository canary; final tracked artifacts will be
regenerated from the clean implementation commit.
