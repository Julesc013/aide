# Boot Slice Definition

## Selected Feature Set

The first boot slice contains two feature ids:

- `boot.slice.invoke`
- `boot.slice.editor-marker`

`boot.slice.invoke` is mandatory for every committed lane.

`boot.slice.editor-marker` is the `L2` extension of the same slice. It is required only where lane acceptance marks editor interaction as required. Elsewhere it may be optional, replaced by a fallback proof, or explicitly deferred.

## Mandatory Behaviors

Every lane must eventually provide these behaviors to achieve the boot slice:

1. expose one user-invokable or companion entry point
2. identify the host family, technology lane, support mode, and host version id when available
3. return a deterministic boot-slice report artifact or equivalent observable output
4. report current capability, target capability, and unavailable reasons honestly
5. preserve deterministic request and response semantics across execution modes

## Optional Or Conditional Behaviors

The slice allows one conditional `L2` proof:

- if the lane can provide `selection_context.active_text`, it may compute and either apply or preview a deterministic editor marker transform

The transform rule for the slice is:

- input: `selection_context.active_text`
- output: `AIDE_BOOT: ` prefixed to that exact text

Example:

- input: `value`
- output: `AIDE_BOOT: value`

If active text is unavailable, the lane must not invent it. It must return an explicit unavailable or deferred result instead.

## Deterministic Inputs And Outputs

### Required Inputs

- canonical lane identity
- execution mode
- requested feature id

### Conditional Inputs

- `selection_context.active_text` for `boot.slice.editor-marker`

### Required Outputs

- stable request id
- boot-slice report artifact or equivalent structured output
- current and target capability values
- available and unavailable behavior list
- diagnostics when the requested behavior is not available

### Conditional Outputs

- one deterministic edit or edit preview for `boot.slice.editor-marker`

## Success Criteria

A lane has achieved the boot slice when:

- its chosen entry point can invoke `boot.slice.invoke`
- the invocation produces deterministic observable output
- the output identifies the lane honestly
- the output includes capability reporting or explicit unavailable reasons
- any required lane-specific `L2` proof defined in `lane-acceptance.md` is satisfied

## Failure, Deferred, And Blocked Reporting

- Use `deferred` when a richer proof is intentionally postponed but the lane can still satisfy its minimum accepted proof.
- Use `blocked` when the lane cannot honestly expose the minimum proof because of a real environment, packaging, contract, or tooling blocker.
- Use explicit unavailable reasons such as `not-implemented`, `host-ceiling`, `missing-context`, `execution-mode-mismatch`, or `blocked`.

## Completion Rule Per Lane

Lane completion is not identical across all hosts.

- Some lanes complete the slice with `L1` report-first proof plus explicit `L2` deferral.
- Some lanes require the `L2` editor marker because the documented public surface is explicitly editor-centric.
- Companion lanes may complete the slice with report-first or report-only proof when that is the honest first shape.

The acceptance table is authoritative for those differences.
