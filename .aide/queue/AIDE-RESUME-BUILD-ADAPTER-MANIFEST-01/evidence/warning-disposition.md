# Warning Disposition

Non-blocking warnings:

- AdapterManifest is not accepted by this build task.
- No adapter admission or trust exists.
- No adapter execution, worker launch, sandbox creation, credential resolution,
  provider/model call, network call, GitHub mutation, patch apply, or target
  repository mutation exists.
- Validation uses a minimal local subset plus semantic checks, not full JSON
  Schema Draft compliance.

These warnings do not block independent check because the slice fails closed and
does not claim execution authority.
