# Profile Binding Review

The result binds to exactly:

```text
aide://conformance-profile/minimal_capability_manifest-v1.0.0
```

The helper fails closed if the loaded profile has a different kind, profile ref,
profile id, version, subject ref, lifecycle shape, or empty case inventory.

The result also records the subject ref:

```text
aide://capability/minimal_capability_manifest
```

No profile activation or subject admission is performed by this binding.
