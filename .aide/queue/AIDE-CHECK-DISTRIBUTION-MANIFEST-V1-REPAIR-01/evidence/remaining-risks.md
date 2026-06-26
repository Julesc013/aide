# Remaining Risks

```json
{
  "material_findings": [
    {
      "category": "protocol_range",
      "description": "A future-major maximum must not be accepted merely because current v1 is inside the numeric interval.",
      "evidence_refs": [
        "protocol-range-review.md"
      ],
      "expected": "distribution.unsupported_protocol_range unless explicit future-major support exists",
      "id": "protocol.future_major_not_implicitly_accepted",
      "observed": {
        "codes": [],
        "range": {
          "max": "2.x",
          "min": "1.0.0"
        },
        "valid": true
      },
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "protocol.range_semantics_incomplete"
    },
    {
      "category": "contamination",
      "description": "Forbidden source-state categories are classified, including export-pack target-root members under files/.",
      "evidence_refs": [
        "contamination-review.md"
      ],
      "expected": "observed forbidden reason for every independently forbidden path",
      "id": "contamination.forbidden_path_classification_complete",
      "observed": [
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide.local/",
          "path": ".aide.local/state.sqlite"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": ".env"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": "raw-prompt.txt"
        },
        {
          "expected": "forbidden_exact",
          "observed": "forbidden_exact_member",
          "path": "raw-response.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/context/latest-",
          "path": ".aide/context/latest-task-packet.md"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/reports/",
          "path": ".aide/reports/distribution-manifest-v1/manifest.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/repo/latest-",
          "path": ".aide/repo/latest-inventory.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/roots/latest-",
          "path": ".aide/roots/latest-classification.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/tools/latest-",
          "path": ".aide/tools/latest-tools.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/install/latest-",
          "path": ".aide/install/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/repair/latest-",
          "path": ".aide/repair/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/upgrade/latest-",
          "path": ".aide/upgrade/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/rollback/latest-",
          "path": ".aide/rollback/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.aide/uninstall/latest-",
          "path": ".aide/uninstall/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:logs/",
          "path": "logs/run.log"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:.cache/",
          "path": ".cache/cache.bin"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "forbidden_prefix:secrets/",
          "path": "secrets/token.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide.local/state.sqlite"
        },
        {
          "expected": "forbidden_exact",
          "observed": "secret_like_member",
          "path": "files/.env"
        },
        {
          "expected": "forbidden_exact",
          "observed": null,
          "path": "files/raw-prompt.txt"
        },
        {
          "expected": "forbidden_exact",
          "observed": null,
          "path": "files/raw-response.txt"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/context/latest-task-packet.md"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/reports/distribution-manifest-v1/manifest.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/repo/latest-inventory.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/roots/latest-classification.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/tools/latest-tools.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/install/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/repair/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/upgrade/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/rollback/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.aide/uninstall/latest-plan.json"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/logs/run.log"
        },
        {
          "expected": "forbidden_prefix",
          "observed": null,
          "path": "files/.cache/cache.bin"
        },
        {
          "expected": "forbidden_prefix",
          "observed": "secret_like_member",
          "path": "files/secrets/token.txt"
        }
      ],
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "contamination.forbidden_members_silently_filtered"
    },
    {
      "category": "contamination",
      "description": "Local-directory forbidden members are recorded instead of silently producing a clean digest.",
      "evidence_refs": [
        "contamination-review.md"
      ],
      "expected": "dirty and nested-dirty directories have forbidden members",
      "id": "contamination.directory_forbidden_members_recorded",
      "observed": {
        "clean_forbidden": 0,
        "dirty_forbidden": 1,
        "nested_dirty_forbidden": 0
      },
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "contamination.forbidden_members_silently_filtered"
    },
    {
      "category": "fixture_coverage",
      "description": "Fixture corpus covers future-major protocol max declarations.",
      "evidence_refs": [
        "fixture-coverage-review.md"
      ],
      "expected": "direct invalid future-major protocol fixture",
      "id": "fixture.future_major_protocol_fixture_present",
      "observed": [],
      "outcome": "FAIL",
      "severity": "material",
      "source_finding_id": "fixture.required_coverage_incomplete"
    }
  ],
  "warnings": []
}
```
