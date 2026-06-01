# Policy And Schema Evidence

Implemented source-of-truth files:

- Policies: `test-tiers`, `impacted-tests`, `test-telemetry`, `full-discovery-handoff`, `test-summary-reduction`, `validation-promotion-gates`.
- Schemas: test tier, impact map, test plan, test summary, test run, full-discovery handoff, failure family, slow-test report, validation-tier report.
- Templates/examples: target test manifest, target impact map, compact summary examples, failure family example, slow-test report example, full-discovery handoff example.
- Docs: validation tier model, test telemetry contracts, impacted-test planning, full-discovery handoff, promotion validation gates.

`py -3 .aide/scripts/aide_lite.py validate` confirms the X-TEST-00 policy anchors, schema shape, examples, and generated outputs.
