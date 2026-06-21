# Registry Projection Review

```json
{
  "diagnostics": {
    "has_source_registry_digest": false,
    "native_count": 129,
    "projected_count": 8,
    "result": "REQUEST_CHANGES",
    "summary": {
      "native_count": 129,
      "omitted_count": 121,
      "omitted_ids_sha256": "sha256:0ac045417b59cb21b4d3aae03b30be958009a5535c5ab6af62af2fe85b779d79",
      "projected_count": 8,
      "projected_ids": [
        "dominium.diagnostic.repo.layout_violation",
        "dominium.diagnostic.repo.forbidden_root",
        "dominium.diagnostic.repo.dependency_direction_violation",
        "dominium.diagnostic.abi.public_header_violation",
        "dominium.diagnostic.public_surface.invalid",
        "dominium.diagnostic.command.invalid_input",
        "dominium.diagnostic.command.unsupported_surface",
        "dominium.diagnostic.capability.missing"
      ],
      "selection_limit": 8,
      "selection_policy": "source_order_first_n",
      "source_registry_path": "contracts/diagnostic/diagnostic_code.registry.json",
      "truncation_disclosed": true
    }
  },
  "refusals": {
    "has_source_registry_digest": false,
    "native_count": 77,
    "projected_count": 8,
    "result": "REQUEST_CHANGES",
    "summary": {
      "native_count": 77,
      "omitted_count": 69,
      "omitted_ids_sha256": "sha256:426206db7961689839a406ea1cfe44cf65c5a44829ea414b5c02b1943d024487",
      "projected_count": 8,
      "projected_ids": [
        "dominium.refusal.validation.invalid_target",
        "dominium.refusal.validation.target_unknown",
        "dominium.refusal.validation.target_kind_unsupported",
        "dominium.refusal.validation.target_outside_allowed_root",
        "dominium.refusal.validation.tool_unavailable",
        "dominium.refusal.capability.missing",
        "dominium.refusal.capability.version_unsupported",
        "dominium.refusal.capability.conflict"
      ],
      "selection_limit": 8,
      "selection_policy": "source_order_first_n",
      "source_registry_path": "contracts/refusal/refusal_code.registry.json",
      "truncation_disclosed": true
    }
  }
}
```
