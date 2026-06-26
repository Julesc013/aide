# No Overclaiming Review

```json
{
  "non_capabilities": {
    "false_boundary": {
      "install_apply_implemented": false,
      "network_calls_implemented": false,
      "provider_model_calls_implemented": false,
      "release_publication_implemented": false,
      "repair_apply_implemented": false,
      "rollback_apply_implemented": false,
      "target_repository_mutation_implemented": false,
      "uninstall_apply_implemented": false,
      "update_apply_implemented": false
    }
  },
  "signature_sbom": {
    "sbom_refs": [
      {
        "reason": "Q47 local bundle does not generate an SBOM artifact.",
        "sbom_ref": "aide://distribution/sbom/unavailable",
        "status": "unavailable"
      }
    ],
    "signature_records": [
      {
        "reason": "Q47 local bundle is not signed.",
        "signature_ref": "aide://distribution/signature/unsigned-placeholder",
        "status": "unsigned",
        "verified": false
      }
    ]
  }
}
```
