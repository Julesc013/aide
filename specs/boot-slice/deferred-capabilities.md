# Deferred Capabilities

The following capabilities are intentionally outside the first boot slice:

## Project And Workspace Awareness

`L3` behavior depends on project-model access that is not uniformly available across the committed lanes. It belongs in a later wave after the first entry-point and report contract is proven.

## Deep IDE UI Integration

`L4` behavior is host-specific and the least portable. It would distort the first wave away from the shared contract proof.

## Semantic Or Multi-File Transformations

The first slice uses a deterministic plain-text marker instead of semantic transforms, refactors, or multi-file edits. Those later features need stronger context models and richer evals.

## Build, Debug, And Toolchain Orchestration

These workflows depend on workspace awareness, environment maturity, and host-specific runtime glue. They are deliberately deferred.

## Release And Packaging Automation

Packaging posture exists in the repository, but real packaging automation is not part of the first cross-host implementation wave.

## Environment Reconstruction Depth

Historical lanes may need deep environment work, but the first slice only requires enough environment evidence to support honest blocked or degraded results.
