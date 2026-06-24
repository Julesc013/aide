# Implementation Summary

The repair keeps the provider domain-neutral and fail-closed:

- Validates invocation, binding, provider id, spec provider ref, capability ref,
  provider spec ref, decoder id, state probe id, scrubber id, and conformance
  profile ref before launch.
- Refuses binding mismatches with `transport_refused`, `not_started`,
  `not_decoded`, `binding_mismatch`, and incomplete evidence.
- Records current invocation launch metadata instead of the first launch in a
  reused provider instance.
- Reports `launcher_call_count: 1` for each valid invocation receipt.
- Treats decoder exceptions, timeouts, and undecoded outcomes as incomplete
  validation/evidence axes.
- Treats state-probe failures as `state_probe_failure`, skips domain decoding,
  and returns no typed domain result.
- Declares process cancellation unsupported in v0.

No live Dominium command was rerun.
